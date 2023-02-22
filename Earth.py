
from cosapp.base import System

from Rocket import Rocket
from Trajectory import Trajectory
from Gravity import Gravity
from Atmosphere import Atmosphere

class Earth(System):
    
    def setup(self):
        
        #Earth children
        self.add_child(Rocket('Rocket'))
        self.add_child(Trajectory('Traj'))
        self.add_child(Gravity('Grav'))
        self.add_child(Atmosphere('Atmo'))
        
        self.connect(self.Rocket, self.Traj, {'v_out' : 'v'})
        self.connect(self.Rocket, self.Grav, ['g'])
        self.connect(self.Traj, self.Grav, {'r' : 'r_in'})
        self.connect(self.Traj, self.Atmo, {'r' : 'r_in'})
        self.connect(self.Atmo, self.Rocket, ['rho'])

        #Execution order
        self.exec_order = ['Grav', 'Atmo', 'Rocket', 'Traj']
