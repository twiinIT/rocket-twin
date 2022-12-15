from cosapp.base import System
from ReferentialPort import ReferentialPort
from Utility import thrust
import numpy as np

class Thrust(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
        
        self.add_inward('m', 1., desc = "Rocket's mass") # We import the mass just in order to update the inputs. Otherwise, the inputs would stay the same and the driver would call compute only one time.

        #Pushing outputs
        self.add_output(ReferentialPort, 'Fp') # desc = "Thrust Force"
        self.add_outward('Mp', 0, desc = "Thrust Moment")


    def compute(self):
        #the data used comes from the experimental values measured on the engine used by X20
        #Fp is a dim2 np.array
        self.Fp.vector = np.array([0, - thrust(self.time)])
