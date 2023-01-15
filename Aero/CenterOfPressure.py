from cosapp.base import System

import numpy as np

class CenterOfPressure(System):
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")

        #CenterOfPressure outputs
        self.add_outward('gf', np.array([0., 0., 8.]), desc = "GF Distance", unit = 'm')  #Distance between propellers and CoP
        
    