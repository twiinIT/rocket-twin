
from cosapp.base import System

from Rocket import Rocket
from Trajectory import Trajectory
from Gravity import Gravity
from Wind import Wind
from Atmosphere.Atmosphere import Atmosphere
from Parachute import Parachute
import numpy as np

class Earth(System):
    
    def setup(self):
        
        #Earth children
        self.add_child(Rocket('Rocket'))
        self.add_child(Trajectory('Traj'))
        self.add_child(Gravity('Grav'))
        self.add_child(Atmosphere('Atmo'))
        self.add_child(Wind('Wind'))
        self.add_child(Parachute('Para'))
        

        
        self.connect(self.Traj, self.Grav, {'r_out' : 'r_in'})
        self.connect(self.Traj, self.Atmo, {'r_out' : 'r_in', 'ParaDep' : 'ParaDep'})
        self.connect(self.Traj, self.Wind, {'r_out' : 'r', 'ParaDep' : 'ParaDep'})
        self.connect(self.Traj, self.Para, {'r_out' : 'r_in', 'ParaDep' : 'ParaDep', 'l0' : 'l0'})

        self.connect(self.Rocket, self.Traj, {'v_out' : 'v', 'Kin_ang' : 'ang', 'ParaDep' : 'ParaDep'})
        self.connect(self.Rocket, self.Grav, ['g'])
        self.connect(self.Wind, self.Rocket, ['v_wind'])
        self.connect(self.Atmo, self.Rocket, ['rho'])
        self.connect(self.Para, self.Grav, ['g'])
        self.connect(self.Rocket, self.Para, {'v_out' : 'v_in'})
        self.connect(self.Wind, self.Para, ['v_wind'])
        self.connect(self.Atmo, self.Para, {'r2_in' : 'r2_out', 'rho' : 'rho'})

        #Execution order
        self.exec_order = ['Traj', 'Grav', 'Atmo', 'Rocket', 'Wind', 'Para']


        self.add_inward('pitch_init', -np.pi/2 + 0.1)
        self.add_inward('yaw_init', np.pi/4)

    def compute(self):
        # print(self.time)
        if self.time == 0:
            self.Rocket.Kin.ar = np.array([0.0, self.pitch_init, self.yaw_init])