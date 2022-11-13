import numpy as np
from cosapp.base import System
from Utility import thrust

class Thrust(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('theta', 0., desc = "Rocket's direction")
        self.add_inward('m', 1., desc = "Rocket's mass")

        #Pushing outputs
        self.add_outward('F', 1., desc = "Thrust Force")
        
    def compute(self):
        self.F = thrust(self.time, self.theta)