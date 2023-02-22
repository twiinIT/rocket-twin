from cosapp.base import System

import numpy as np

class Moments(System):
    def setup(self):
        #AeroForces inward
        self.add_inward('F', np.zeros(3) , desc='Aerodynamic Forces', unit='N')

        #Geometry inwards
        self.add_inward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')

        #Outward
        self.add_outward('Ma', np.zeros(3) , desc='Aerodynamic Moments', unit='N*m')

    def compute(self):

        OM = np.array([self.l/2 - self.Xcp, 0, 0]) 

        self.Ma = np.cross(OM,self.F)
