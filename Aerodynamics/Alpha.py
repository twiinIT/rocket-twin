from cosapp.base import System

import numpy as np

class Alpha(System):
    def setup(self):
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 
        self.add_outward('alpha', 0., desc='angle of attack', unit='') 

    def compute(self):
        self.alpha = np.arccos(self.v_cpa[0]/np.linalg.norm(self.v_cpa)) if np.linalg.norm(self.v_cpa)>0.1 else 0
