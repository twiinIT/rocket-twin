from cosapp.base import System

import numpy as np

class Dimensions(System):
    
    def setup(self):
        
        #Dimensions outputs
        self.add_outward('l', 10., desc = "Rocket Length", unit = 'm')
        self.add_outward('r_cyl', 0.05, desc = "Rocket Radius", unit = 'm')
        self.add_outward('S', 0.01, desc = "Propeller Surface", unit = 'm**2')
        self.add_outward('S_ref', 1., desc = "Rocket Surface of Reference", unit = 'm**2')
        
    def compute(self):
        
        self.S_ref = np.pi*self.r_cyl**2
        