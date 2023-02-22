from cosapp.base import System

from Alpha import Alpha
from Aeroforces import AeroForces
from Coefficients import Coefficients
from Moments import Moments

import numpy as np

class Aerodynamics(System):
    def setup(self):
        #System orientation
        self.add_inward('Aero_ang', np.zeros(3), desc = "Rocket Euler Angles")
        
        #Geometry
        #TODO Create a mass System
        self.add_inward('m', desc = "mass", unit = 'kg')

        
        self.add_outward('F', np.zeros(3), desc = "Aerodynamics Forces", unit = 'N')
        self.add_outward('Ma', np.zeros(3), desc = "Aerodynamics Moments", unit = 'N*m')
                

        self.add_child(Alpha('Alpha'), pulling=['v_cpa'])
        self.add_child(AeroForces('Aeroforces'), pulling=['v_cpa', 'F','rho'])
        self.add_child(Coefficients('Coefs'), pulling=['v_cpa', 'l'])
        self.add_child(Moments('Moments'), pulling=['Ma'])

        self.connect(self.Alpha, self.Coefs, ['alpha'])
        self.connect(self.Coefs, self.Aeroforces, ['Cd', 'Cn','S_ref'])
        self.connect(self.Coefs, self.Moments, ['Xcp', 'l'])
        self.connect(self.Aeroforces, self.Moments, ['F'])


        self.exec_order = ['Alpha', 'Coefs', 'Aeroforces', 'Moments']
