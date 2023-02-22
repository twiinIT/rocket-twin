from cosapp.base import System

import numpy as np

class AeroForces(System):
    def setup(self):
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 

        #Coefficients inwards
        self.add_inward('Cd', 0., desc='Drag coefficient', unit='')
        self.add_inward('Cn', 0., desc='Normal coefficient', unit='')
        self.add_inward('S_ref', 1., desc="Reference Surface", unit="m**2")

        #Atmosphere
        self.add_inward('rho', 1.292, unit="kg/m**3")

        self.add_outward('F', np.zeros(3) , desc='Aerodynamic Forces', unit='N')

    def compute(self):

        angle = np.arccos(self.v_cpa[0]/np.linalg.norm(self.v_cpa)) if np.linalg.norm(self.v_cpa)>0.1 else 0 #angle d'attaque
        
        Ca0 = .5
        Cn0 = 0

        Ca_alpha = .1
        Cn_alpha = 2

        Ca = Ca_alpha * angle + Ca0 
        Cn = Cn_alpha * angle + Cn0 

        Fa = .5 * self.rho * np.linalg.norm(self.v_cpa)**2 * self.S_ref * Ca
        Fn = .5 * self.rho * np.linalg.norm(self.v_cpa)**2 * self.S_ref * Cn

        a = np.arctan2(self.v_cpa[2], self.v_cpa[1])

        Fnz = - Fn*np.sin(a)
        Fny = - Fn*np.cos(a)

        self.F = [-Fa, Fny, Fnz]
