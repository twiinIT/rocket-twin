from cosapp.base import System

import numpy as np

class Coefficients(System):
    
    def setup(self):
        
        #System inputs
        self.add_inward('Cx0', 1., desc = "X Axis Initial Aerodynamic Coefficient", unit = '')
        self.add_inward('Cy0', 0., desc = "Y Axis Initial Aerodynamic Coefficient", unit = '')
        self.add_inward('Cz0', 0., desc = "Z Axis Initial Aerodynamic Coefficient", unit = '')
        
        self.add_inward('Cy_beta', 1., desc = "Cy Rate of Change", unit = '')
        self.add_inward('Cz_alpha', 1., desc = "Cz Rate of Change", unit = '')
        
        #Angles inputs
        self.add_inward('alpha', 0., desc = "Angle of Attack", unit = '')
        self.add_inward('beta', 0., desc = "Angle of Bank", unit = '')
        
        #Coefficients outputs
        self.add_outward('C', np.zeros(3), desc = "Aerodynamics Coefficient", unit = '')
        
    def compute(self):
        
        self.C[1] = self.Cy0 + self.Cy_beta*self.beta
        self.C[2] = self.Cz0 + self.Cz_alpha*self.alpha
        self.C[0] = self.Cx0 + 0.5*self.C[2]*self.alpha
    