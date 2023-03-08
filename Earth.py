
from cosapp.base import System

from Rocket import Rocket
from Trajectory import Trajectory
from Gravity import Gravity
from Atmosphere.Wind import Wind
from Atmosphere.Atmosphere import Atmosphere
from Mass import Mass

class Earth(System):
    
    def setup(self):
        
        #Earth children
        self.add_child(Rocket('Rocket'))
        self.add_child(Trajectory('Traj'))
        self.add_child(Gravity('Grav'))
        self.add_child(Atmosphere('Atmo'))
        #self.add_child(Mass('Mass'))
        
        self.connect(self.Rocket, self.Traj, {'v_out' : 'v'})
        self.connect(self.Rocket, self.Grav, ['g'])
        self.connect(self.Traj, self.Grav, {'r_out' : 'r_in'})
        self.connect(self.Traj, self.Atmo, {'r_out' : 'r_in'})
        self.connect(self.Atmo,self.Rocket, ['v_wind','rho'])
        #self.connect(self.Rocket, self.Mass, {'m' : 'm_out', 'I':'I'})

        #Execution order
        self.exec_order = ['Grav', 'Atmo', 'Rocket', 'Traj']
