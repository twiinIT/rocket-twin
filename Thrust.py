from cosapp.base import System

from Utility import thrust

import numpy as np

class Thrust(System):
    
    def setup(self):
        
        #System constants
        self.add_inward('g0', 9.81, desc = "Gravity at Earth's Surface", unit = 'm/s**2')
        self.add_inward('isp', 100., desc = "Specific Impulsion in vacuum", unit = 's')
        
        #Rocket inputs
        self.add_inward('qp', 10., desc = "Engine's Propulsive Debt", unit = 'kg/s')
        
        #Pressure inputs
        self.add_inward('P', 100000., desc = "Atmospheric Pressure at Rocket's Height", unit = 'Pa')
        
        #Geometry inputs
        self.add_inward('S', 0.01, desc = "Propeller Area", unit = 'm**2')
        
        #Thrust outputs
        self.add_outward('Fp', np.zeros(3), desc = "Thrust Force", unit = 'N')
        self.add_outward('Mp', np.zeros(3), desc = "Thrust Moment", unit = 'N*m')
        
    def compute(self):

        self.Fp[0] = thrust(self.time)
        self.Fp[1] = 0.
        self.Fp[2] = 0.
        
        self.Mp[0] = 0.
        self.Mp[1] = 0.
        self.Mp[2] = 0.
        
        