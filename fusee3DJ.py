import numpy as np
from cosapp.base import System, Port, BaseConnector


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



###Kinematics


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
        self.add_outward('av_out', np.zeros(3), desc = "Rocket Angular Velocity (pqr)", unit = '1/s')
        
    def compute(self):

        # l1 = np.array([np.cos(self.ar[1])*np.cos(self.ar[2]), -np.sin(self.ar[2]), 0.])
        # l2 = np.array([np.cos(self.ar[1])*np.sin(self.ar[2]),  np.cos(self.ar[2]), 0.])
        # l3 = np.array([-np.sin(self.ar[1]), 0, 1])
        # A = np.array([l1,l2,l3])

        # self.av2 = np.matmul(np.linalg.inv(A), self.av)
        # print('aa : ') 
        # print(self.aa)  
        # print('av : ') 
        # print(self.av) 
        # print('av2 : ')
        # print(self.av2)
        # print('ar : ') 
        # print(self.ar)

        #compute angular velocity to obtain angular position
        self.av2[0] = self.av[0] + np.tan(self.ar[1])*(self.av[2]*np.cos(self.ar[0]) + self.av[1]*np.sin(self.ar[0]))
        self.av2[1] = self.av[1]*np.cos(self.ar[0]) - self.av[2]*np.sin(self.ar[0])
        self.av2[2] = (self.av[2]*np.cos(self.ar[0]) + self.av[1]*np.sin(self.ar[0]))/(np.cos(self.ar[1]))

        # print(self.av2)

        self.v_out.val = self.v
        self.av_out = self.av
        self.Kin_ang = self.ar



###Thrust

import pandas as pd


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

        


###Dynamics


class Dynamics(System):
    def setup(self):
    
        #System orientation
        self.add_inward('Dyn_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Kinematics inputs
        self.add_input(VelPort, 'v_in')
        self.add_inward('av_in', np.zeros(3), desc = "Rocket Angular Velocity", unit = '1/s')
        
        
        # #AeroForces inputs
        # self.add_inward('Fa', np.zeros(3), desc = "Thrust Force", unit = 'N')
        # self.add_inward('Ma', np.zeros(3), desc = "Aerodynamic Moment", unit = 'N*m')
        
        # #Geometry inputs
        # self.add_inward('m', 100., desc = "Rocket Mass", unit = 'kg')
        # self.add_inward('I', np.array([10., 100., 100.]), desc = "Rocket Moments of Inertia", unit = 'kg*m**2')
        
        #Gravity inputs
        self.add_input(AclPort, 'g')
        
        #Dynamics outputs
        self.add_outward('a', np.zeros(3), desc = "Rocket Acceleration", unit = 'm/s**2')
        self.add_outward('aa', np.zeros(3), desc = "Rocket Angular Acceleration", unit = '1/s**2')
        
    def compute(self):

        m = 15
        I = np.array([10., 100., 100.])
        
        v = self.v_in.val
        av = self.av_in

        Fp = thrust(self.time)
        
        self.a[0] = Fp/m + self.g.val[0] + av[2]*v[1] - av[1]*v[2]
        self.a[1] = self.g.val[1] + av[0]*v[2] - av[2]*v[0]
        self.a[2] = self.g.val[2] + av[1]*v[0] - av[0]*v[1]
        
        self.aa[0] =  (I[1] - I[2])*av[1]*av[2]/I[0]
        self.aa[1] =   (I[2] - I[0])*av[2]*av[0]/I[1]
        self.aa[2] =  (I[0] - I[1])*av[0]*av[1]/I[2]

        
###Aero

class Aerodynamics(System):
    def setup(self):
        
        self.add


###Trajectory


class Trajectory(System):
    
    def setup(self):
    
        #Rocket inputs
        self.add_inward('v', np.zeros(3), desc = "Rocket Velocity", unit = 'm/s')
        
        #Trajectory transients
        self.add_transient('r', der = 'v', desc = "Rocket Position")
        


###Rocket   


class Rocket(System):
    
    def setup(self):

        #System orientation
        self.add_inward('Rocket_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        #Rocket children
        self.add_child(Kinematics('Kin'), pulling = ['v_out'])
        self.add_child(Dynamics('Dyn'), pulling = ['g'])
        
        #Child-Child connections
        self.connect(self.Kin, self.Dyn, {'Kin_ang' : 'Dyn_ang', 'v_out' : 'v_in', 'av_out' : 'av_in', 'a': 'a', 'aa' : 'aa'})
        # self.connect(self.Dyn, self.Aero, ['Fa', 'Ma'])
        
        #Execution order
        self.exec_order = ['Dyn', 'Kin']



###Gravity



class Gravity(System):
    
    def setup(self):
        #Gravity outputs
        self.add_output(AclPort, 'g')
        
    def compute(self):
        
        # self.g.val = np.array([0., 0., self.G*self.M/(self.R - self.r_in[2])**2])
        self.g.val = np.array([0, 0, -9.8])



###Earth


class Earth(System):
    
    def setup(self):
        
        #Earth children
        self.add_child(Rocket('Rocket'))
        self.add_child(Trajectory('Traj'))
        self.add_child(Gravity('Grav'))
        
        self.connect(self.Rocket, self.Traj, {'v_out.val' : 'v'})
        self.connect(self.Rocket, self.Grav, ['g'])
        
        #Execution order
        self.exec_order = ['Grav', 'Rocket', 'Traj']



###Main




from cosapp.drivers import RungeKutta, NonLinearSolver
import plotly.graph_objs as go
from cosapp.recorders import DataFrameRecorder

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
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Kin.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp', 'Rocket.Kin.Kin_ang', 'Rocket.Kin.av', 'Rocket.Aero.V_wind.val']),
    period=1,
)

#Initial conditions and constants

l = 10 #Rocket's length

driver.set_scenario(
    init = {
        'Traj.r' : np.array([0., 0., l/2]),
        'Rocket.Kin.v' : np.zeros(3),
        'Rocket.Kin.ar' : np.array([np.pi/6, -np.pi/2 + 0.1, np.pi/4]),
        'Rocket.Kin.av' : np.zeros(3),
    },
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
        zaxis = dict(nticks=2, range=[0,2000],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))


fig.show()

#useful library zhen using euler angle
from scipy.spatial.transform import Rotation as R



traj_topx = []
traj_topz = []
traj_botx = []
traj_botz = []
traj_topy = []
traj_boty = []

l=100
rocket = np.array([l,0,0]) #representation of the rocket as a 3D vector that will be rotated and translated according to the computed trajectory

rock = []

for i in range(len(traj)):
    rotation = R.from_euler('xyz', ang[i], degrees=False)
    rotation.apply(rocket)
    rock.append(rotation.apply(rocket))

rock = np.asarray(rock)

traj_bot = traj #traj[time][xyz]
traj_top = traj + rock

traj_topx = np.asarray(traj_topx)
traj_botx = np.asarray(traj_botx)
traj_topz = np.asarray(traj_topz)
traj_botz = np.asarray(traj_botz)

# #print(traj_topy, traj_boty)

# for i in range(len(traj_top)):
#     print("Traj", (traj_top[i][0]-traj_bot[i][0])**2 + (traj_top[i][1]-traj_bot[i][1])**2)


#Plot results

#Animation - Rocket's movement


fig2 = go.Figure(data=[go.Scatter3d(x=[traj_bot[0][0], traj_top[0][0]], y=[traj_bot[0][1], traj_top[0][1]], z=[traj_bot[0][2], traj_top[0][2]])])

fig2.update_layout(title='Rocket Movement',
                  scene=dict(
            xaxis=dict(range=[-500, 500], autorange=False),
            yaxis=dict(range=[-500, 500], autorange=False),
            zaxis=dict(range=[0, 2000], autorange=False),
        ),
                  updatemenus=[dict(buttons = [dict(
                                               args = [None, {"frame": {"duration": 20, 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 10}}],
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