import numpy as np
from cosapp.base import System

class Dynamics(System):
    
    def setup(self):
        
        #Pushing inputs
        self.add_inward('F', np.zeros(2), desc="Thrust Force")

        #Aerodynamic inputs
        self.add_inward('Fa', np.zeros(2), desc="Aerodynamic Force")
        self.add_inward('Ma', 0., desc="Aerodynamic Moment")

        #Mass inputs
        self.add_inward('m', 1., desc="Rocket Mass")
        self.add_inward('I', 1.475e-3, desc="Moment of Inertia")

        #Gravity inputs
        self.add_inward('g', np.array([0, -9.8]), desc="Gravity")

        #Trajectory Outputs
        self.add_outward('a', np.zeros(2), desc = "Rocket Acceleration")
        self.add_outward('aw', 0., desc = "Rocket Angular Acceleration")
    
        
    def compute(self):
        
        wind = np.array([0, 0])

        self.a = (self.F + self.Fa + wind)/self.m + self.g
        self.aw = (self.Ma)/self.I