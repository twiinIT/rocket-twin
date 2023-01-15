from cosapp.base import System

from Aerodynamics import Aerodynamics
from Thrust import Thrust
from Geometry import Geometry 
from Dynamics import Dynamics
from Kinematics import Kinematics

import numpy as np


class Rocket(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")

        #System orientation
        self.add_inward('Rocket_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
    
        #Engine propulsive debt
        self.add_inward('qp', 10., desc = "Engine's Propulsive Debt", unit = 'kg/s')
        
        #Rocket children
        self.add_child(Kinematics('Kin'), pulling = ['v_out'])
        self.add_child(Dynamics('Dyn'), pulling = ['g'])
        self.add_child(Thrust('Thrust'), pulling = ['P', 'qp'])
        self.add_child(Geometry('Geom'), pulling = ['qp'])
        self.add_child(Aerodynamics('Aero'), pulling = ['V_wind', 'rho'])
        
        #Child-Child connections
        self.connect(self.Kin, self.Dyn, {'Kin_ang' : 'Dyn_ang', 'v_out' : 'v_in', 'av_out' : 'av_in', 'a': 'a', 'aa' : 'aa'})
        self.connect(self.Kin, self.Aero, {'v_out' : 'v_in', 'Kin_ang' : 'Aero_ang'})
        self.connect(self.Dyn, self.Thrust, ['Fp', 'Mp'])
        self.connect(self.Dyn, self.Geom, {'m' : 'm_out', 'I' : 'I'})
        self.connect(self.Dyn, self.Aero, ['Fa', 'Ma'])
        self.connect(self.Geom, self.Aero, ['S_ref', 'gc'])
        
        #Execution order
        self.exec_order = ['Geom', 'Thrust', 'Aero', 'Dyn', 'Kin']

