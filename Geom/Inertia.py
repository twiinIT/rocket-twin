from cosapp.base import System

import numpy as np

class Inertia(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
    
        #Mass inputs
        self.add_inward('m_in', 100., desc = "Rocket Mass", unit = 'kg')
        
        #Dimensions inputs
        self.add_inward('l', 10., desc = "Rocket Length", unit = 'm')
        self.add_inward('r_cyl', 0.05, desc = "Rocket Radius", unit = 'm')
        
        #Inertia outputs
        self.add_outward('I', np.zeros(3), desc = "Rocket Moments of Inertia", unit = 'kg*m**2')
        
    def compute(self):
        
        self.I[0] = self.m_in*self.r_cyl**2/2
        self.I[1] = self.m_in*self.l**2/12
        self.I[2] = self.m_in*self.l**2/12
        
        