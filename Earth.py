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
        
        self.connect(self.Rocket, self.Traj, {'v_out.val' : 'v'})
        self.connect(self.Rocket, self.Grav, ['g'])
        self.connect(self.Rocket, self.Atmo, ['P', 'V_wind', 'rho'])
        self.connect(self.Grav, self.Traj, {'r_in' : 'r_out'})
        self.connect(self.Atmo, self.Traj, {'r_in' : 'r_out'})
        
        #Execution order
        self.exec_order = ['Grav', 'Atmo', 'Rocket', 'Traj']
