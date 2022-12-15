from cosapp.base import System

from ReferentialPort import ReferentialPort

import numpy as np

class Dynamics(System):
    
    def setup(self):
        
        #Thrust inputs
        self.add_inward('referential', 'Earth', desc = "Dynamics is in the Earth's referential")

        self.add_input(ReferentialPort, 'Fp') # desc = "Thrust Force"
        self.add_inward('Mp', np.zeros(2), desc = "Thrust Moment")

        #Aerodynamic inputs
        self.add_input(ReferentialPort, 'Fa') # desc = "Aerodynamic Force"
        self.add_inward('Ma', 0., desc = "Aerodynamic Moment")

        #Mass inputs
        self.add_inward('m', 1., desc = "Rocket Mass")
        self.add_inward('I', 1.475e-3, desc = "Moment of Inertia")

        #Gravity inputs
        self.add_inward('g', np.array([0, -9.8]), desc = "Gravity")

        #Trajectory Outputs
        self.add_outward('a', np.zeros(2), desc = "Rocket Acceleration")
        self.add_outward('aw', 0., desc = "Rocket Angular Acceleration")
    
        
    def compute(self):

        self.a = (self.Fp.vector + self.Fa.vector) / self.m + self.g
        self.aw = (self.Ma + self.Mp) / self.I

        # print(f'{self.Fp=}')
        # print(f'{self.Fa=}')
        # print(f'{self.a=}')
        # print(f'{self.m=}')
