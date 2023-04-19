from cosapp.base import System

import numpy as np

class Pressure(System):
    
    def setup(self):
        
        #System constants
        self.add_inward('P0', 97500., desc = "Atmospheric Pressure at Sea Level", unit = 'Pa')
        self.add_inward('T0', 298., desc = "Temperature at Sea Level", unit = 'K')
        
        #Trajectory inputs
        self.add_inward('r_in', np.zeros(3), desc = "Rocket's Position", unit = 'm')

        #Parachute inputs
        self.add_inward('r2_in', np.zeros(3), desc = "Lower String's Position", unit = 'm')
        self.add_inward_modevar('ParaDep', 1., desc = "Parachute Deployed", unit = '')
        
        #Pressure outputs
        self.add_outward('P', 101325., desc = "Atmospheric Pressure at Rocket's Height", unit = 'Pa')
        
    def compute(self):
        #Linear temperature evolution in the atmosphere. Formula found on wikipedia
        #The typical temperature gradient is -0.0065 in the troposphere
        if self.ParaDep == 0:
            self.P = self.P0 * (1 - (0.0065 * self.r_in[2])/self.T0)**5.226
        else:
            self.P = self.P0 * (1 - (0.0065 * self.r2_in[2])/self.T0)**5.226