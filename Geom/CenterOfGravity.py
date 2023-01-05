from cosapp.base import System

import numpy as np

class CenterOfGravity(System):
    
    def setup(self):
        
        #Dimensions inputs
        self.add_inward('l', 10., desc = "Rocket Length", unit = 'm')
        
        #CenterOfGravity outputs
        self.add_outward('gc', np.zeros(3), desc = "GC Distance", unit = 'm')  #Distance between the propellers and the CoG
        
    def compute(self):
        
        self.gc = np.array([0., 0., self.l/2])
        