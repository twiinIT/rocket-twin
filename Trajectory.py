from cosapp.base import System

import numpy as np

class Trajectory(System):
    
    def setup(self):
        self.add_inward('referential', 'Earth', desc = "Earth's referential")
    
        #Rocket inputs
        self.add_inward('v', np.zeros(3), desc = "Rocket Velocity", unit = 'm/s')
        
        #Trajectory transients
        self.add_transient('r', der = 'v', desc = "Rocket Position")
        
        #Trajectory outputs
        self.add_outward('r_out', np.zeros(3), desc = "Rocket Position", unit = 'm')
        
    def compute(self):
        
        self.r_out = self.r
        