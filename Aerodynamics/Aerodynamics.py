from cosapp.base import System

from Aerodynamics.Aeroforces import AeroForces
from Aerodynamics.Coefficients import Coefficients
from Aerodynamics.Moments import Moments

from Ports import VelPort

import numpy as np

class Aerodynamics(System):
    def setup(self):
        #System orientation
        self.add_inward('Aero_ang', np.zeros(3), desc = "Rocket Euler Angles")
        
        #Geometry
        #TODO Create a mass System
        self.add_inward('m', desc = "mass", unit = 'kg')

        self.add_input(VelPort, 'v_wind')
            
        self.add_outward('F', np.zeros(3), desc = "Aerodynamics Forces", unit = 'N')
        self.add_outward('Ma', np.zeros(3), desc = "Aerodynamics Moments", unit = 'N*m')
                

        self.add_child(AeroForces('Aeroforces'), pulling=['v_cpa', 'F','rho', 'v_wind'])
        self.add_child(Coefficients('Coefs'), pulling=['v_cpa', 'l', 'rho', 'v_wind', 'av'])
        self.add_child(Moments('Moments'), pulling=['Ma'])

        self.connect(self.Coefs, self.Aeroforces, ['Cd', 'N','S_ref'])
        self.connect(self.Coefs, self.Moments, ['Xcp', 'l', 'M', 'Mroll'])
        self.connect(self.Aeroforces, self.Moments, ['F'])


        self.exec_order = ['Coefs', 'Aeroforces', 'Moments']
