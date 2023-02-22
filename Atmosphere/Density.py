from cosapp.base import System

import numpy as np

class Density(System):
    
    def setup(self):
        
        #System constants
        self.add_inward('rho0', 1.225, desc = "Air Density at Sea Level", unit = 'kg/m**3')
        self.add_inward('T0', 298., desc = "Temperature at Sea Level", unit = 'K')
        
        #Trajectory inputs
        self.add_inward('r_in', np.zeros(3), desc = "Rocket's Position", unit = 'm')
        
        #Density outputs
        self.add_outward('rho', 1.225, desc = "Air Density at Rocket's Height", unit = 'kg/m**3')
        
        
    def compute(self):
        #Linear temperature evolution in the atmosphere. Formula found on wikipedia
        #The typical temperature gradient is -0.0065 in the troposphere
        self.rho = self.rho0 * (1 - (0.0065 * self.r_in[2])/self.T0)**5.226
        print(self.rho)