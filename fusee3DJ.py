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
        self.add_inward('Fa', np.zeros(3), desc = "Thrust Force", unit = 'N')
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
        self.a[0] = (self.Fa[0] + Fp)/self.m + self.g.val[0] + av[2]*v[1] - av[1]*v[2]
        self.a[1] = self.Fa[1]/self.m + self.g.val[1] + av[0]*v[2] - av[2]*v[0]
        self.a[2] = self.Fa[2]/self.m + self.g.val[2] + av[1]*v[0] - av[0]*v[1]
        
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

        self.add_outward('Fa', np.zeros(3) , desc='Aerodynamic Forces', unit='N')

    def compute(self):



        Fn = 0.5*self.rho*np.linalg.norm(self.v_cpa)**2*self.Cn*self.S_ref
        Fd = 0.5*self.rho*np.linalg.norm(self.v_cpa)**2*self.Cd*self.S_ref

        print(Fn, Fd)

        #alpha and beta are the angles defined in the Rapport intermédiaire
        alpha = np.arctan2(self.v_cpa[2], self.v_cpa[0]) # Maybe should be with a - ?
        beta = np.arctan2(self.v_cpa[1], self.v_cpa[0])




        # Check polar coordinates formulas
        Fd_vector = np.array([-Fd*np.cos(alpha)*np.cos(beta),
                            -Fd*np.cos(alpha)*np.sin(beta),
                            -Fd*np.sin(alpha)])
        
        angle = np.arctan2(self.v_cpa[2], self.v_cpa[1])
        Fn_vector = np.array([0,
                            -Fn*np.sin(angle),
                            -Fn*np.cos(angle)])
        self.Fa = Fd_vector + Fn_vector




class Moments(System):
    def setup(self):
        #AeroForces inward
        self.add_inward('Fa', np.zeros(3) , desc='Aerodynamic Forces', unit='N')

        #Geometry inwards
        self.add_inward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')

        #Outward
        self.add_outward('Ma', np.zeros(3) , desc='Aerodynamic Moments', unit='N*m')

    def compute(self):

        OM = np.array([self.l/2 - self.Xcp, 0, 0])

        self.Ma = np.cross(OM, self.Fa)



class Aerodynamics(System):
    def setup(self):
        #System orientation
        self.add_inward('Aero_ang', np.zeros(3), desc = "Rocket Euler Angles")
        
        #Geometry
        #TODO Create a mass System
        self.add_inward('m', desc = "mass", unit = 'kg')

        
        self.add_outward('Fa', np.zeros(3), desc = "Aerodynamics Forces", unit = 'N')
        self.add_outward('Ma', np.zeros(3), desc = "Aerodynamics Moments", unit = 'N*m')
                

        self.add_child(Alpha('Alpha'), pulling=['v_cpa'])
        self.add_child(AeroForces('Aeroforces'), pulling=['v_cpa', 'Fa'])
        self.add_child(Coefficients('Coefs'), pulling=['v_cpa', 'l'])
        self.add_child(Moments('Moments'), pulling=['Ma'])

        self.connect(self.Alpha, self.Coefs, ['alpha'])
        self.connect(self.Coefs, self.Aeroforces, ['Cd', 'Cn','S_ref'])
        self.connect(self.Coefs, self.Moments, ['Xcp', 'l'])
        self.connect(self.Aeroforces, self.Moments, ['Fa'])


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
        self.connect(self.Dyn, self.Aero, ['Fa', 'Ma'])
        
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
dt = 0.1

#Create System
earth = Earth('earth')

#Add RungeKutta driver
driver = earth.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 40)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))


# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Kin.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp', 'Rocket.Kin.Kin_ang', 'Rocket.Kin.av', 'Rocket.aeroforces.']),
    period=1,
)

#Initial conditions and constants

l = 100 #Rocket's length on the plot

driver.set_scenario(
    init = {
        'Traj.r' : np.array([0., 0., l/2]),
        'Rocket.Kin.v' : np.array([1,0,0.5]),
        'Rocket.Kin.ar' : np.array([np.pi/6, -np.pi/2 + 0.1, 0]),
        'Rocket.Kin.av' : np.zeros(3),
    },
    stop='Traj.r[2]<0'

    )


earth.run_drivers()

# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
traj = np.asarray(data['Traj.r'].tolist())
velo = np.asarray(data['Rocket.Kin.v'].tolist())
acel = np.asarray(data['Rocket.Kin.a'].tolist())
ang = np.asarray(data['Rocket.Kin.Kin_ang'].tolist())
avelo = np.asarray(data['Rocket.Kin.av'].tolist())

#Plot results

x=[]
y=[]
z=[]
theta = []

for i in range(len(traj)):
    x.append(traj[i][0])
    y.append(traj[i][1])
    z.append(traj[i][2])

for i in range(len(ang)):
    theta.append(ang[1])

fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    marker=dict(
        size=4,
        color=z,
        colorscale='Viridis',
    ),
    line=dict(
        color='darkblue',
        width=2
    )
))


fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=2, range=[-1000,1000],),
        yaxis = dict(nticks=2, range=[-1000,1000],),
        zaxis = dict(nticks=2, range=[0,1000],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))


fig.show()

#useful library zhen using euler angle


rocket = np.array([l,0,0]) #representation of the rocket as a 3D vector that will be rotated and translated according to the computed trajectory

rock = []

for i in range(len(traj)):
    rotation = R.from_euler('xyz', ang[i], degrees=False)
    rotation.apply(rocket)
    rock.append(rotation.apply(rocket))

rock = np.asarray(rock)

traj_bot = traj #traj[time][xyz]
traj_top = traj + rock


#Animation - Rocket's movement
fig2 = go.Figure(data=[go.Scatter3d(x=[traj_bot[0][0], traj_top[0][0]], y=[traj_bot[0][1], traj_top[0][1]], z=[traj_bot[0][2], traj_top[0][2]])])

fig2.update_layout(title='Rocket Movement',
                  scene=dict(
            xaxis=dict(range=[-1000, 1000], autorange=False),
            yaxis=dict(range=[-1000, 1000], autorange=False),
            zaxis=dict(range=[0, 1000], autorange=False),
        ),
                  updatemenus=[dict(buttons = [dict(
                                               args = [None, {"frame": {"duration": 100, 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 100}}],
                                               label = "Play",
                                               method = "animate")],
                                type='buttons',
                                showactive=False,
                                y=1,
                                x=1.12,
                                xanchor='right',
                                yanchor='top')])

frames= [go.Frame(data=[go.Scatter3d(x=[traj_bot[i][0], traj_top[i][0]], y=[traj_bot[i][1], traj_top[i][1]], z=[traj_bot[i][2], traj_top[i][2]])]) for i in range(len(traj))]
fig2.update(frames=frames)

fig2.show()