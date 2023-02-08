import numpy as np
import pandas as pd
import plotly.graph_objs as go
from cosapp.base import System, Port, BaseConnector
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from scipy.spatial.transform import Rotation as R

###PORTS
def RotMat3D(ang):
    
    #ang[0] = phi, ang[1] = theta, ang[2] = psi
    #rotation matrix to go from R0 (earth frame) to R (rocket frame)
    
    l1 = np.array([np.cos(ang[2])*np.cos(ang[1]), np.sin(ang[2])*np.cos(ang[1]), -np.sin(ang[1])])
    l2 = np.array([-np.sin(ang[2])*np.cos(ang[0]) + np.cos(ang[2])*np.sin(ang[1])*np.sin(ang[0]), 
                    np.cos(ang[2])*np.cos(ang[0]) + np.sin(ang[2])*np.sin(ang[1])*np.sin(ang[0]), np.cos(ang[1])*np.sin(ang[0])])
    l3 = np.array([ np.sin(ang[2])*np.sin(ang[0]) + np.cos(ang[2])*np.sin(ang[1])*np.cos(ang[0]), 
                   -np.cos(ang[2])*np.sin(ang[0]) + np.sin(ang[2])*np.sin(ang[1])*np.cos(ang[0]), np.cos(ang[1])*np.cos(ang[0])])
    
    A = np.round(np.array([l1,l2,l3]), 5)
    
    return A


class VelPort(Port):
    """Velocity Port """
    def setup(self):
        self.add_variable('val', np.zeros(3), desc = "Velocity Components", unit = 'm/s')
        

    class Connector(BaseConnector):
        """Custom connector for `VelPort` objects
        """
        def __init__(self, name: str, sink: Port, source: Port, *args, **kwargs):
            super().__init__(name, sink, source)

        def transfer(self) -> None:
            sink = self.sink
            source = self.source
            
            #Parent --> Child
            if sink.owner.parent == source.owner:
                sink.val = np.matmul(RotMat3D(sink.owner[f'{sink.owner.name}_ang']), source.val)

            #Child --> Parent
            elif sink.owner == source.owner.parent:
                sink.val = np.matmul(np.transpose(RotMat3D(source.owner[f'{source.owner.name}_ang'])), source.val)
                
            else:
                sink.val = source.val



class AclPort(Port):
    """Acceleration Port """
    def setup(self):
        self.add_variable('val', np.zeros(3), desc = "Acceleration Components", unit = 'm/s**2')
        

    class Connector(BaseConnector):
        """Custom connector for `AclPort` objects
        """
        def __init__(self, name: str, sink: Port, source: Port, *args, **kwargs):
            super().__init__(name, sink, source)

        def transfer(self) -> None:
            sink = self.sink
            source = self.source

            #Parent --> Child
            if sink.owner.parent == source.owner:
                sink.val = np.matmul((RotMat3D(sink.owner[f'{sink.owner.name}_ang'])), source.val)

            #Child --> Parent
            elif sink.owner == source.owner.parent:
                sink.val = np.matmul(np.transpose(RotMat3D(source.owner[f'{source.owner.name}_ang'])), source.val)
                
            else:
                sink.val = source.val


###KINEMATICS
class Kinematics(System):
    
    def setup(self):
    
        #System orientation
        self.add_outward('Kin_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Dynamics inputs
        self.add_inward('a', np.zeros(3), desc = "Rocket Acceleration", unit = 'm/s**2')
        self.add_inward('aa', np.zeros(3), desc = "Rocket Angular Acceleration", unit = '1/s**2')
        self.add_outward('av2', np.zeros(3), desc = "Rocket Angular Velocity", unit = '1/s')
        
        #Kinematics transients
        self.add_transient('v', der = 'a', desc = "Rocket Velocity")
        self.add_transient('av', der = 'aa', desc = "Rocket Angular Velocity (pqr)")
        self.add_transient('ar', der = 'av2', desc = "Rocket Angular Position")
        
        #Kinematics outputs
        self.add_output(VelPort, 'v_out')
        self.add_outward('v_cpa',  np.zeros(3), desc='CPA velocity', unit = 'm/s')
        self.add_outward('av_out', np.zeros(3), desc = "Rocket Angular Velocity (pqr)", unit = '1/s')
        
    def compute(self):
        #compute angular velocity to obtain angular position
        self.av2[0] = self.av[0] + np.tan(self.ar[1])*(self.av[2]*np.cos(self.ar[0]) + self.av[1]*np.sin(self.ar[0]))
        self.av2[1] = self.av[1]*np.cos(self.ar[0]) - self.av[2]*np.sin(self.ar[0])
        self.av2[2] = (self.av[2]*np.cos(self.ar[0]) + self.av[1]*np.sin(self.ar[0]))/(np.cos(self.ar[1]))

        self.v_out.val = self.v

        self.av_out = self.av
        self.Kin_ang = self.ar
        self.v_cpa = self.v


###THRUST
thrust_data = pd.read_csv("thrust.txt", header=None)
times = list(thrust_data.iloc[0])
thrusts = list(thrust_data.iloc[1])

def mean(x, y, fx, fy, t):
    """Calculates the linear regression between x and y and evaluates it at t"""
    percent = (t - x)/(y - x)
    return (fx + (fy - fx)*percent)


def thrust(time):
    """Calculates the thrust of the rocket"""

    #If the time is superior to the last data point there is no more thrust
    if time >= times[-1]:
        return 0

    i=0
    while times[i] <= time:
        i += 1

    return mean(times[i - 1], times[i], thrusts[i - 1], thrusts[i], time) 


###DYNAMICS
class Dynamics(System):
    def setup(self):
    
        #System orientation
        self.add_inward('Dyn_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Geometry
        self.add_inward('l', desc = "Rocket length", unit = 'm')
        self.add_inward('I', desc = "Matrix of inertia")
        self.add_inward('m', desc = "mass", unit = 'kg')
        
        #Kinematics inputs
        self.add_input(VelPort, 'v_in')
        self.add_inward('av_in', np.zeros(3), desc = "Rocket Angular Velocity", unit = '1/s')
        
        #AeroForces inputs
        self.add_inward('F', np.zeros(3), desc = "Thrust Force", unit = 'N')
        self.add_inward('Ma', np.zeros(3), desc = "Aerodynamic Moment", unit = 'N*m')
        
        #Gravity inputs
        self.add_input(AclPort, 'g')
        
        #Dynamics outputs
        self.add_outward('a', np.zeros(3), desc = "Rocket Acceleration", unit = 'm/s**2')
        self.add_outward('aa', np.zeros(3), desc = "Rocket Angular Acceleration", unit = '1/s**2')
        
    def compute(self):

        I = self.I
        
        v = self.v_in.val
        av = self.av_in

        Fp = thrust(self.time)

        
        #Acceleration
        self.a[0] = (self.F[0] + Fp)/self.m + self.g.val[0] + av[2]*v[1] - av[1]*v[2]
        self.a[1] = self.F[1]/self.m + self.g.val[1] + av[0]*v[2] - av[2]*v[0]
        self.a[2] = self.F[2]/self.m + self.g.val[2] + av[1]*v[0] - av[0]*v[1]
        
        #Angular acceleration (no momentum associated to thrust)
        self.aa[0] = (self.Ma[0] + (I[1] - I[2])*av[1]*av[2])/I[0] 
        self.aa[1] = (self.Ma[1] + (I[2] - I[0])*av[2]*av[0])/I[1]
        self.aa[2] = (self.Ma[2] + (I[0] - I[1])*av[0]*av[1])/I[2]


class Alpha(System):
    def setup(self):
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 
        self.add_outward('alpha', 0., desc='angle of attack', unit='') 

    def compute(self):
        self.alpha = np.arccos(self.v_cpa[0]/np.linalg.norm(self.v_cpa)) if np.linalg.norm(self.v_cpa)>0.1 else 0


class Coefficients(System):
    def setup(self):
        self.add_inward('alpha', 0., desc='angle of attack', unit='') 
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 

        # Rocket's Geometry
        self.add_inward('ln', 0.2, desc="Length of the cone", unit='m')
        self.add_inward('dn', 0.15, desc='Rocket caliber', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')
        self.add_inward('xf', self.l - 0.2, desc = "Rocket minus fins length", unit = 'm')

        #Fins' Geometry, check the plan for explanation
        self.add_inward('lr', 0.16, unit = 'm')
        self.add_inward('lt', 0.12, unit='m')
        self.add_inward('ls', 0.12, unit = 'm')
        self.add_inward('lw', 0.05, unit = 'm')
        self.add_inward('lm', 0.2, unit = 'm')
        self.add_inward('lts', 2*self.ls + self.dn, unit = 'm')
        self.add_inward('tf', 0.005, desc = 'Thickness', unit='m')
        
        #Coefficients outwards
        self.add_outward('Cd', 0., desc='Drag coefficient', unit='')
        self.add_outward('Cn', 0., desc='Normal coefficient', unit='')
        self.add_outward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_outward('S_ref', np.pi*(self.dn/2)**2, desc="Reference Surface", unit="m**2")


    def compute(self):

        if np.linalg.norm(self.v_cpa)>10:
            cna_c = 2
            cna_b = 0
            cna_f = (1 + self.dn/(self.ls + self.dn/2))*4*4*(self.ls/self.dn)**2/(1 + (1 + 2*self.lm/(self.lr + self.lt))**0.5)
            cna = cna_c + cna_b + cna_f

            self.Cn = cna*self.alpha

            self.Xcp = 1/cna*(cna_c*2/3*self.ln + cna_f*(self.xf + self.lm*(self.lr + 2*self.lt)/(3*(self.lr+self.lt)) + 1/6*(self.lr + self.lt - self.lr*self.lt/(self.lr+self.lt))))

            Rec = 5*10**5
            Ref =  Rec #np.linalg.norm(self.v_cpa) * self.l / (15.6*10**(-6))
            Refb = Rec #np.linalg.norm(self.v_cpa) * self.lm / (15.6*10**(-6))

            Bf = Rec * (0.074/Ref**0.2) - 1.328/Ref**0.5
            Bfb = Rec * (0.074/Refb**0.2) - 1.328/Refb**0.5

            cffb = 1.328/Refb**0.5 if Refb < Rec else 0.074/Refb**0.2 - Bfb/Refb
            cff = 1.328/Ref**0.5 if Ref < Rec else 0.074/Ref**0.2 - Bf/Ref

            afe = 1/2 * (self.lr + self.lt)*self.ls
            afb = afe + 0.5*self.dn*self.lr
            cdi = 2*cff*(1+2*self.tf/self.lm)*4*4*(afb - afe)/(np.pi*self.dn**2)
            cdf = 2*cff*(1+2*self.tf/self.lm)*4*4*(afb)/(np.pi*self.dn**2)
            cdfb = (1 + 60/(self.l/self.dn)**3 + 0.0025*self.l/self.dn)*(2.7*self.l/self.dn + 4*self.l/self.dn)*(cffb)
            cdb = 0.029/cdfb**0.5
            cd0 = cdfb + cdb + cdf + cdi
            cdba = 2*0.9*self.alpha**2 + 3.6*0.7*(1.36*self.l - 0.55*self.ln)/(np.pi*self.dn)*self.alpha**3
            rs = self.lts/self.dn
            kfb = 0.8065*rs**2 + 1.1553*rs
            kbf = 0.1935*rs**2 + 0.8174*rs + 1
            cdfa = self.alpha**2*(1.2*afb**4/(np.pi*self.dn**2) + 3.12*(kfb + kbf - 1)*afe**4/(np.pi*self.dn**2))
            self.Cd = cd0 + cdba + cdfa 



class AeroForces(System):
    def setup(self):
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 

        #Coefficients inwards
        self.add_inward('Cd', 0., desc='Drag coefficient', unit='')
        self.add_inward('Cn', 0., desc='Normal coefficient', unit='')
        self.add_inward('S_ref', 1., desc="Reference Surface", unit="m**2")

        #Atmosphere
        self.add_inward('rho', 1.292, unit="kg/m**3")

        self.add_outward('F', np.zeros(3) , desc='Aerodynamic Forces', unit='N')

    def compute(self):

        angle = np.arccos(self.v_cpa[0]/np.linalg.norm(self.v_cpa)) if np.linalg.norm(self.v_cpa)>0.1 else 0 #angle d'attaque
        
        Ca0 = .5
        Cn0 = 0

        Ca_alpha = .1
        Cn_alpha = 2

        Ca = Ca_alpha * angle + Ca0 
        Cn = Cn_alpha * angle + Cn0 

        Fa = .5 * self.rho * np.linalg.norm(self.v_cpa)**2 * self.S_ref * Ca
        Fn = .5 * self.rho * np.linalg.norm(self.v_cpa)**2 * self.S_ref * Cn

        a = np.arctan2(self.v_cpa[2], self.v_cpa[1])

        Fnz = - Fn*np.sin(a)
        Fny = - Fn*np.cos(a)

        self.F = [-Fa, Fny, Fnz]





class Moments(System):
    def setup(self):
        #AeroForces inward
        self.add_inward('F', np.zeros(3) , desc='Aerodynamic Forces', unit='N')

        #Geometry inwards
        self.add_inward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')

        #Outward
        self.add_outward('Ma', np.zeros(3) , desc='Aerodynamic Moments', unit='N*m')

    def compute(self):

        OM = np.array([self.l/2 - self.Xcp, 0, 0]) 

        self.Ma = np.cross(OM,self.F)
        self.Ma[0] = 2



class Aerodynamics(System):
    def setup(self):
        #System orientation
        self.add_inward('Aero_ang', np.zeros(3), desc = "Rocket Euler Angles")
        
        #Geometry
        #TODO Create a mass System
        self.add_inward('m', desc = "mass", unit = 'kg')

        
        self.add_outward('F', np.zeros(3), desc = "Aerodynamics Forces", unit = 'N')
        self.add_outward('Ma', np.zeros(3), desc = "Aerodynamics Moments", unit = 'N*m')
                

        self.add_child(Alpha('Alpha'), pulling=['v_cpa'])
        self.add_child(AeroForces('Aeroforces'), pulling=['v_cpa', 'F'])
        self.add_child(Coefficients('Coefs'), pulling=['v_cpa', 'l'])
        self.add_child(Moments('Moments'), pulling=['Ma'])

        self.connect(self.Alpha, self.Coefs, ['alpha'])
        self.connect(self.Coefs, self.Aeroforces, ['Cd', 'Cn','S_ref'])
        self.connect(self.Coefs, self.Moments, ['Xcp', 'l'])
        self.connect(self.Aeroforces, self.Moments, ['F'])


        self.exec_order = ['Alpha', 'Coefs', 'Aeroforces', 'Moments']



###TRAJECTORY
class Trajectory(System):
    
    def setup(self):
    
        #Rocket inputs
        self.add_input(VelPort, 'v')
        
        #Trajectory transients
        self.add_transient('r', der = 'v.val', desc = "Rocket Position")



###ROCKET
class Rocket(System):
    
    def setup(self):

        #System orientation
        self.add_inward('Rocket_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        #Gravity input
        self.add_input(AclPort, 'g')
        
        #Rocket parameters
        self.add_inward('l', 2., desc='Rocket length', unit='m')
        self.add_inward('I', np.array([10., 100., 100.]), desc = "Matrix of inertia")
        self.add_inward('m', 15, desc = "mass", unit = 'kg')

        #Rocket children
        self.add_child(Kinematics('Kin'), pulling = ['v_out'])
        self.add_child(Dynamics('Dyn'), pulling = ['g', 'l', 'I', 'm'])
        self.add_child(Aerodynamics('Aero'), pulling = ['l', 'm'])
        
        #Child-Child connections
        self.connect(self.Kin, self.Dyn, {'Kin_ang' : 'Dyn_ang', 'v_out' : 'v_in', 'a': 'a', 'aa' : 'aa'})
        self.connect(self.Kin, self.Aero, {'Kin_ang' : 'Aero_ang', 'v_cpa':'v_cpa'})
        self.connect(self.Dyn, self.Aero, ['F', 'Ma'])
        
        #Execution order
        self.exec_order = ['Aero', 'Dyn', 'Kin']



###GRAVITY
class Gravity(System):
    
    def setup(self):
        #Gravity outputs
        self.add_output(AclPort, 'g')
        
    def compute(self):
        
        # self.g.val = np.array([0., 0., self.G*self.M/(self.R - self.r_in[2])**2])
        self.g.val = np.array([0, 0, -9.8])



###EARTH
class Earth(System):
    
    def setup(self):
        
        #Earth children
        self.add_child(Rocket('Rocket'))
        self.add_child(Trajectory('Traj'))
        self.add_child(Gravity('Grav'))
        
        self.connect(self.Rocket, self.Traj, {'v_out' : 'v'})
        self.connect(self.Rocket, self.Grav, ['g'])
        
        #Execution order
        self.exec_order = ['Grav', 'Rocket', 'Traj']


###MAIN
#Time-step
dt = 0.05

#Create System
earth = Earth('earth')

#Add RungeKutta driver
driver = earth.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 40)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))


# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Kin.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp', 'Rocket.Kin.Kin_ang', 'Rocket.Kin.av', 'Rocket.Aero.F', 'Traj.v.val']),
    period=.1,
)

#Initial conditions and constants

l = 10 #Rocket's length on the plot

driver.set_scenario(
    init = {
        'Traj.r' : np.array([0., 0., l/2]),
        'Rocket.Kin.v' : np.array([0,0,0]),
        'Rocket.Kin.ar' : np.array([np.pi/6, -np.pi/2 + .2, np.pi/4]),
        'Rocket.Kin.av' : np.zeros(3),
    },
    stop='Traj.v.val[2]<-1'

    )


earth.run_drivers()








#==================================
# Rocket's trajectory visualisation 
#==================================

import os
import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import animation
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.proj3d import proj_transform


#==================================
# INPUTS
# t : time 
# T : thrust 
# r : position
# v : velocity in rocket's referential
# a : acceleration in rocket's referential
# phi, theta, psi : euler angles
#===================================

# ==============================
# vector equations

def vector_derivative(vector, wrt):
    """
    differentiate vector components wrt a symbolic variable
    param v: vector to differentiate
    param wrt: symbolic variable
    return V: velcoity vector and components in x, y, z
    """
    return [component.diff(wrt) for component in vector]


def vector_magnitude(vector):
    """
    compute magnitude of a vector
    param vector: vector with components of Cartesian form
    return magnitude: magnitude of vector
    """
    # NOTE: np.linalg.norm(v) computes Euclidean norm
    magnitude = 0
    for component in vector:
        magnitude += component ** 2
    return magnitude ** (1 / 2)


def unit_vector(from_vector_and_magnitude=None, from_othogonal_vectors=None, from_orthogonal_unit_vectors=None):
    """
    Calculate a unit vector using one of three input parameters.
    1. using vector and vector magnitude
    2. using orthogonal vectors
    3. using orthogonal unit vectors
    """

    if from_vector_and_magnitude is not None:
        vector_a, magnitude = from_vector_and_magnitude[0], from_vector_and_magnitude[1]
        return [component / magnitude for component in vector_a]

    if from_othogonal_vectors is not None:
        vector_a, vector_b = from_othogonal_vectors[0], from_othogonal_vectors[1]
        vector_normal = np.cross(vector_a, vector_b)
        return unit_vector(from_vector_and_magnitude=(vector_normal, vector_magnitude(vector_normal)))

    if from_orthogonal_unit_vectors is not None:
        u1, u2 = from_orthogonal_unit_vectors[0], from_orthogonal_unit_vectors[1]
        return np.cross(u1, u2)


def evaluate_vector(vector, time_step):
    """
    evaluate numerical vector components and magnitude @ti
    param numerical_vector: symbolic vector expression to evaluate @ti
    param ti: time step for evaluation
    return magnitude, numerical_vector: magnitude of vector and components evaluated @ti
    """
    numerical_vector = [float(component.subs(t, time_step).evalf()) for component in vector]
    magnitude = vector_magnitude(numerical_vector)
    return numerical_vector, magnitude


def direction_angles(vector, magnitude=None):
    """
    compute direction angles a vector makes with +x,y,z axes
    param vector: vector with x, y, z components
    param magnitude: magnitude of vector
    """
    magnitude = vector_magnitude(vector) if magnitude is None else magnitude
    return [sp.acos(component / magnitude) for component in vector]

# ==============================
# helper functions


def d2r(degrees):
    """
    convert from degrees to radians
    return: radians
    """
    return degrees * (np.pi / 180)


def r2d(radians):
    """
    convert from radians to degrees
    return: degrees
    """
    return radians * (180 / np.pi)



#==================================
# Create Dataframe
#==================================


# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
r = np.asarray(data['Traj.r'].tolist())
v = np.asarray(data['Rocket.Kin.v'].tolist())
a = np.asarray(data['Rocket.Kin.a'].tolist())
euler = np.asarray(data['Rocket.Kin.Kin_ang'].tolist())

#Modélisation de l'axe de la fusée et de sa normale(grossie x5)
rocket = np.array([l*8,0,0])
y = np.array([0,l*5,0])
z = np.array([0,0,l*5])

indy = []
indz = []
rock = []
for i in range(len(r)):
    rotation = R.from_euler('xyz', euler[i], degrees=False)
    vect1 = rotation.apply(rocket)
    vect2 = rotation.apply(y)
    vect3 = rotation.apply(z)
    norm_v1 = vector_magnitude(vect1)
    norm_v2 = vector_magnitude(vect2)
    norm_v2 = vector_magnitude(vect3)
    for b in vect1:
        b = b/norm_v1
    for c in vect2:
        c = c/norm_v2
    for d in vect2:
        d = d/norm_v2
    rock.append(vect1)
    indy.append(vect2)
    indz.append(vect3)

rock = np.asarray(rock)
indy = np.asarray(indy)
indz = np.asarray(indz)


rt = rock


propagation_time_history = []


i = 0
for ti in time:
    iteration_results = {'t': ti, 
                         'rx': r[i][0], 'ry': r[i][1], 'rz': r[i][2],
                         'vx': v[i][0], 'vy': v[i][1], 'vz': v[i][2],
                         'ax': a[i][0], 'ay': a[i][1], 'az': a[i][2],
                         'rtx': rt[i][0], 'rty': rt[i][1], 'rtz': rt[i][2],
                         'indyx': indy[i][0], 'indyy': indy[i][1], 'indyz': indy[i][2],
                         'indzx': indz[i][0], 'indzy': indz[i][1], 'indzz': indz[i][2]
                        }
    i+=1
    propagation_time_history.append(iteration_results)

df = pd.DataFrame(propagation_time_history)


#==================================
# Visualise trajectory
#==================================

# Arrow3D used for drawing arrow as vectors in 3D space
class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)
        
    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs) 


def vector_arrow_3d(x0, x1, y0, y1, z0, z1, color):
    """
    method to create a new arrow in 3d for vectors
    return Arrow3D: new vector
    """
    return Arrow3D(x0, x1, y0, y1, z0, z1,
                   mutation_scale=10, lw=1,
                   arrowstyle='-|>', color=color)


class Animator:

    def __init__(self, simulation_results):
        self.simulation_results = simulation_results
        self.vector_lines = []
        # =======================================
        #  configure plots and data structures

        self.fig = plt.figure(figsize=(15, 8))
        self.fig.subplots_adjust(left=0.05,
                                 bottom=None,
                                 right=0.95,
                                 top=None,
                                 wspace=None,
                                 hspace=0.28)


        self.ax1 = self.fig.add_subplot(projection='3d')

        self.set_axes_limits()

        # axis 1 - 3D visualisation

        self.trajectory, = self.ax1.plot([], [], [], 'bo', markersize=1)


    def draw_xyz_axis(self, x_lims, y_lims, z_lims):
        """
        draw xyz axis on ax1 3d plot
        param x_lims: upper and lower x limits
        param y_lims: upper and lower y limits
        param z_lims: upper and lower z limits
        """
        self.ax1.plot([0, 0], [0, 0], [0, 0], 'ko', label='Origin')
        self.ax1.plot(x_lims, [0, 0], [0, 0], 'k-', lw=1)
        self.ax1.plot([0, 0], y_lims, [0, 0], 'k-', lw=1)
        self.ax1.plot([0, 0], [0, 0], z_lims, 'k-', lw=1)
        self.text_artist_3d('x', 'k', x_lims[1], 0, 0)
        self.text_artist_3d('y', 'k', 0, y_lims[1], 0)
        self.text_artist_3d('z', 'k', 0, 0, z_lims[1])
        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('y')
        self.ax1.set_zlabel('z')

    def text_artist_3d(self, text, color, x=0, y=0, z=0):
        """
        create new text artist for the plot
        param txt: text string
        param color: text color
        param x: x coordinate of text
        param y: y coordinate of text
        param z: z coordinate of text
        """
        return self.ax1.text(x, y, z, text, size=11, color=color)

    def set_axes_limits(self):
        """
        set the axis limits for each plot, label axes
        """
        lim_params = ['r']
        x_lims = self.get_limits(lim_params, 'x')
        y_lims = self.get_limits(lim_params, 'y')
        z_lims = self.get_limits(lim_params, 'z')

        self.ax1.set_xlim3d(x_lims)
        self.ax1.set_ylim3d(y_lims)
        self.ax1.set_zlim3d(z_lims)
        self.draw_xyz_axis(x_lims, y_lims, z_lims)

        t_lims = self.get_limits(['t'], '')



    def get_limits(self, params, axis):
        """
        get upper and lower limits for parameter
        param axis: get limits for axis, i.e x or y
        param params: list of varaible names
        """
        lower_lim, upper_lim = 0, 0
        for p in params:
            m = max(self.simulation_results['%s%s' % (p, axis)])
            if m > upper_lim:
                upper_lim = m
            m = min(self.simulation_results['%s%s' % (p, axis)])
            if m < lower_lim:
                lower_lim = m
            m = max(abs(lower_lim - 0.05), upper_lim + 0.05)
        return lower_lim - 0.05,upper_lim + 0.05

    def config_plots(self):
        """
        Setting the axes properties such as title, limits, labels
        """
        self.ax1.set_title('Trajectory Visualisation')
        self.ax1.set_position([0.25, 0, 0.5, 1])
        self.ax1.set_aspect('equal')

    def visualize(self, i):

        # ######
        # axis 1
        row = self.simulation_results.iloc[i]

        # define vectors
        vectors = [vector_arrow_3d(0, 0, 0, row.rx, row.ry, row.rz, 'g'), 
                   vector_arrow_3d(row.rx, row.ry, row.rz, row.rtx, row.rty, row.rtz, 'r'),
                   vector_arrow_3d(row.rx, row.ry, row.rz, row.indyx, row.indyy, row.indyz, 'k'),
                   vector_arrow_3d(row.rx, row.ry, row.rz, row.indzx, row.indzy, row.indzz, 'k')
                  ]

        # add vectors to figure
        [self.ax1.add_artist(vector) for vector in vectors]

        # remove previous vectors from figure
        if self.vector_lines:
            [vector.remove() for vector in self.vector_lines]
        self.vector_lines = vectors


        # update trajectory for current time step
        self.trajectory.set_data(self.simulation_results['rx'][:i], self.simulation_results['ry'][:i])
        self.trajectory.set_3d_properties(self.simulation_results['rz'][:i])


        # plt.pause(0.05)

    def animate(self):
        """
        animate drawing velocity vector as particle
        moves along trajectory
        return: animation
        """
        return animation.FuncAnimation(self.fig,
                                       self.visualize,
                                       frames=len(time),
                                       init_func=self.config_plots(),
                                       blit=False,
                                       repeat=True,
                                       interval=5)


# =======================================
# save trajectory animation

animator = Animator(simulation_results=df)
anim = animator.animate()
plt.show()

