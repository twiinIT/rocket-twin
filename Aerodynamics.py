from cosapp.base import System

import numpy as np

from Aero.AeroForces import AeroForces
from Aero.RelativeSpeed import RelativeSpeed 
from Aero.Angles import Angles
from Aero.Coefficients import Coefficients
from Aero.CenterOfPressure import CenterOfPressure

class Aerodynamics(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
    
        #System Orientation
        self.add_inward('Aero_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Aerodynamics children
        self.add_child(AeroForces('AeroForces'), pulling = ['Fa', 'Ma', 'rho', 'S_ref', 'gc'])
        self.add_child(RelativeSpeed('RelSpeed'), pulling = ['v_in', 'V_wind'])
        self.add_child(Angles('Angles'))
        self.add_child(Coefficients('Coeff'))
        self.add_child(CenterOfPressure('CoP'))
        
        #Children-children connections
        self.connect(self.RelSpeed, self.Angles, ['V_rel'])
        self.connect(self.Angles, self.Coeff, ['alpha', 'beta'])
        self.connect(self.AeroForces, self.RelSpeed, ['V_rel'])
        self.connect(self.AeroForces, self.Coeff, ['C'])
        self.connect(self.AeroForces, self.CoP, ['gf'])
        
        
        #Execution order
        self.exec_order = ['RelSpeed', 'CoP', 'Angles', 'Coeff', 'AeroForces']
    