from cosapp.base import System
from Utility.Utility import thrust

from scipy.spatial.transform import Rotation as R

import numpy as np

class Thrust(System):
    def setup(self):
        self.add_inward('bang', np.zeros(3), desc="bracage angle", unit="")
        self.add_inward('inclinaison', 0.0)

        #Geometry
        self.add_inward('l', desc = "Rocket length", unit = 'm')
        self.add_inward('CG', desc='Center of Gravity', unit='m')

        #Thrust outputs
        self.add_outward("Fp", np.zeros(3), desc="Thrust Force", unit = 'N')
        self.add_outward('Mp', np.zeros(3), desc="Thrust Moment", unit = 'N*m')

        #Computing artefact
        self.add_transient("useless", der='l', desc="Useless")

    def compute(self):
        self.Fp = np.array([thrust(self.time), 0, 0])
        rot = R.from_euler('xyz', np.array([self.inclinaison, self.inclinaison, self.inclinaison]))
        self.Fp = rot.apply(self.Fp)
        self.Mp = np.cross(np.array([- self.CG, 0, 0]), self.Fp)