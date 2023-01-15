from cosapp.base import System

import numpy as np

class Pressure(System):
    
    def setup(self):
        self.add_inward('referential', 'Earth', desc = "Earth's referential")
        
        #System constants
        self.add_inward('P0', 101325., desc = "Atmospheric Pressure at Sea Level", unit = 'Pa')
        
        #Trajectory inputs
        self.add_inward('r_in', np.zeros(3), desc = "Rocket's Position", unit = 'm')
        
        #Pressure outputs
        self.add_outward('P', 101325., desc = "Atmospheric Pressure at Rocket's Height", unit = 'Pa')
        
    def compute(self):
        
        self.P = self.P0 * (20000. - self.r_in[-1]) / (20000. + self.r_in[-1])
