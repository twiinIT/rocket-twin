from cosapp.base import System

from Ports import VelPort

class Trajectory(System):
    
    def setup(self):
    
        #Rocket inputs
        self.add_input(VelPort, 'v')
        
        #Trajectory transients
        self.add_transient('r', der = 'v.val', desc = "Rocket Position")
