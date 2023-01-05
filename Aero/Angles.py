from cosapp.base import System

import numpy as np

class Angles(System):
    
    def setup(self):
        
        #RelativeSpeed inputs
        self.add_inward('V_rel', np.zeros(3), desc = "Relative Velocity", unit = 'm/s')
        
        #Angles outputs
        self.add_outward('alpha', 0., desc = "Angle of Attack", unit = '')
        self.add_outward('beta', 0., desc = "Angle of Bank", unit = '')
        
    def compute(self):
        
        self.alpha = np.arcsin(self.V_rel[2]/np.linalg.norm(self.V_rel))
        self.beta = np.arcsin(self.V_rel[1]/np.linalg.norm(self.V_rel))
        