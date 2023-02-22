from cosapp.base import System

from Ports import VelPort

import numpy as np 

class Trajectory(System):
    
    def setup(self):
    
        #Rocket inputs
        self.add_input(VelPort, 'v')
        self.add_outward('r_out', np.zeros(3), desc = "Rocket Position", unit="m")

        #Trajectory transients
        self.add_transient('r', der = 'v.val', desc = "Rocket Position")

    def compute(self):
        self.r_out = self.r
