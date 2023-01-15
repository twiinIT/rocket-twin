from cosapp.base import System

import sys
sys.path.append('../rocket-twin')
from Ports import VelPort

import numpy as np

class RelativeSpeed(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")

        #System orientation
        self.add_inward('RelSpeed_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Kinematics inputs
        self.add_input(VelPort, 'v_in')
        
        #Wind inputs
        self.add_input(VelPort, 'V_wind')
        
        #RelativeSpeed outputs
        self.add_outward('V_rel', np.zeros(3), desc = "Relative Velocity", unit = 'm/s')
        
    def compute(self):
        
        self.V_rel = self.V_wind.val - self.v_in.val
        
    