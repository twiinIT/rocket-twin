import numpy as np
from cosapp.base import System
from Utility import thrust

class Thrust(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('theta', 0., desc = "Rocket's direction")
        self.add_inward('m', 1., desc = "Rocket's mass")

        #Pushing outputs
        self.add_outward('Fp', 1., desc = "Thrust Force")
        self.add_outward('Mp', 0, desc = "Thrust Moment")
        
    def compute(self):
        #the data used comes from the experimental values measured on the engine used by X20
        #Fp is a dim2 np.array
        self.Fp = thrust(self.time, self.theta)

