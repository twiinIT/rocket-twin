from cosapp.base import System

import numpy as np

class Moments(System):
    def setup(self):
        #Moments inwards
        self.add_inward('M', 0., desc='Pitch moment')
        self.add_inward('Mroll', 0., desc='Roll  moment')

        #Geometry inwards
        self.add_inward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')

        #Outward
        self.add_outward('Ma', np.zeros(3) , desc='Aerodynamic Moments', unit='N*m')

    def compute(self):
        print(self.M)
        self.Ma[0] = self.Mroll
        self.Ma[1] = self.M
