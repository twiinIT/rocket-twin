from cosapp.base import System

import sys
sys.path.append('../rocket-twin')
from Ports import VelPort

import numpy as np

class Wind(System):
    
    def setup(self):
        
        #System orientation
        self.add_inward('Wind_ang', np.array([0., 0., np.pi/6]))
        
        #Wind inputs
        self.add_inward('V', 5., desc = "Wind Velocity", unit = 'm/s')
        
        #Wind outputs
        self.add_output(VelPort, 'V_wind')
        
    def compute(self):
        
        self.V_wind.val = np.array([self.V, 0., 0.])
        