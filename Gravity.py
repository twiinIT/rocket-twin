from cosapp.base import System

from Ports import AclPort

import numpy as np


class Gravity(System):
    
    def setup(self):
        self.add_inward('referential', 'Earth', desc = "Earth's referential")
        
        #System constants
        self.add_inward('G', 6.6743*10**(-11), desc = "Gravitational Constant", unit = 'N*m**2/kg**2')
        self.add_inward('M', 5.972*10**24, desc = "Earth's Mass", unit = 'kg')
        self.add_inward('R', 6.371*10**6, desc = "Earth's Radius", unit = 'm')
        
        #Trajectory inputs
        self.add_inward('r_in', np.zeros(3), desc = "Rocket Position", unit = 'm')
        
        #Gravity outputs
        self.add_output(AclPort, 'g')
        
    def compute(self):
        
        self.g.val = np.array([0., 0., -self.G*self.M/(self.R + self.r_in[-1])**2])
