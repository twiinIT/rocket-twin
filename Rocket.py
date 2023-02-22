from cosapp.base import System

from Ports import VelPort, AclPort
from Kinematics import Kinematics
from Dynamics import Dynamics
from Thrust import Thrust
from Aerodynamics.Aerodynamics import Aerodynamics

import numpy as np

class Rocket(System):
    
    def setup(self):

        #System orientation
        self.add_inward('Rocket_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        #Gravity input
        self.add_input(AclPort, 'g')
        self.add_input(VelPort, 'v_wind')
        
        #Rocket parameters
        self.add_inward('l', 2., desc='Rocket length', unit='m')
        self.add_inward('I', np.array([10., 100., 100.]), desc = "Matrix of inertia")
        self.add_inward('m', 15, desc = "mass", unit = 'kg')

        #Rocket children
        self.add_child(Kinematics('Kin'), pulling = ['v_out'])
        self.add_child(Dynamics('Dyn'), pulling = ['g', 'l', 'I', 'm'])
        self.add_child(Aerodynamics('Aero'), pulling = ['l', 'm','rho', 'v_wind'])
        self.add_child(Thrust('Thrust'), pulling=['l'])
        
        #Child-Child connections
        self.connect(self.Kin, self.Dyn, {'Kin_ang' : 'Dyn_ang', 'v_out' : 'v_in', 'a': 'a', 'aa' : 'aa'})
        self.connect(self.Kin, self.Aero, {'Kin_ang' : 'Aero_ang', 'v_cpa':'v_cpa'})
        self.connect(self.Dyn, self.Aero, ['F', 'Ma'])
        self.connect(self.Thrust, self.Dyn, ['Fp', 'Mp'])
        
        #Execution order
        self.exec_order = ['Thrust', 'Aero', 'Dyn', 'Kin',]
