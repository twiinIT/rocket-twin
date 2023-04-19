from cosapp.base import System

import numpy as np

class Moments(System):
    def setup(self):
        #Force inward
        self.add_inward('F', np.zeros(3) , desc='Aerodynamic Forces', unit='N')
 
        #Moments inwards
        self.add_inward('M', 0., desc='Pitch moment')
        self.add_inward('Mroll', 0., desc='Roll  moment')

        #Geometry inwards
        self.add_inward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')

        #Outward
        self.add_outward('Ma', np.zeros(3) , desc='Aerodynamic Moments', unit='N*m')

        #Parachute
        self.add_inward('ParaDep', 0., desc = "Parachute Deployed", unit = '')

    def compute(self):
        if self.ParaDep == 1:
            return

        # Lever arm technique
        OM = np.array([self.l/2 - self.Xcp, 0, 0]) 
        self.Ma = np.cross(OM,self.F)
        self.Ma[0] += self.Mroll
