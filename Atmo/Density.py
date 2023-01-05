from cosapp.base import System

import numpy as np

class Density(System):
    
    def setup(self):
        
        #System constants
        self.add_inward('rho0', 1.225, desc = "Air Density at Sea Level", unit = 'kg/m**3')
        
        #Trajectory inputs
        self.add_inward('r_in', np.zeros(3), desc = "Rocket's Position", unit = 'm')
        
        #Density outputs
        self.add_outward('rho', 1.225, desc = "Air Density at Rocket's Height", unit = 'kg/m**3')
        
    def compute(self):
        
        self.rho = self.rho0 * (20000. - self.r_in[-1]) / (20000. + self.r_in[-1])
        