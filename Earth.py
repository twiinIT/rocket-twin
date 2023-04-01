
from cosapp.base import System

from Rocket import Rocket
from Trajectory import Trajectory
from Gravity import Gravity
from Wind import Wind
from Atmosphere.Atmosphere import Atmosphere
from Parachute import Parachute

class Earth(System):
    
    def setup(self):
        
        #Earth children
        self.add_child(Rocket('Rocket'))
        self.add_child(Trajectory('Traj'))
        self.add_child(Gravity('Grav'))
        self.add_child(Atmosphere('Atmo'))
        self.add_child(Wind('Wind'))
        self.add_child(Parachute('Para'))
        

        self.connect(self.Rocket, self.Traj, {'v_out' : 'v'})
        self.connect(self.Rocket, self.Grav, ['g'])
        self.connect(self.Traj, self.Grav, {'r_out' : 'r_in'})
        self.connect(self.Traj, self.Atmo, {'r_out' : 'r_in'})
        self.connect(self.Traj, self.Wind, {'r_out' : 'r'})
        self.connect(self.Wind, self.Rocket, ['v_wind'])
        self.connect(self.Atmo, self.Rocket, ['rho'])
        self.connect(self.Para, self.Grav, ['g'])
        self.connect(self.Rocket, self.Para, {'v_out' : 'v_in', 'Kin_ang':'ang'})
        self.connect(self.Traj, self.Para, {'r_out' : 'r_in'})
        self.connect(self.Wind, self.Para, ['v_wind'])

        #Execution order
        self.exec_order = ['Grav', 'Atmo', 'Rocket', 'Traj', 'Wind', 'Para']
