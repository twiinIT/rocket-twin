from cosapp.base import System
import numpy as np
from rellipsoid import earth

class Gravity(System):

    def setup(self):

        self.add_inward('r', np.zeros(3), desc="Rocket position", unit='m')
        self.add_inward('phi', 0., desc="Rocket latitude", unit='')

        self.add_outward('g', np.zeros(3), desc="Earth's gravity at rocket's height", unit='m/s**2')

    def compute(self):

        self.g[2] = earth.get_analytic_gravity(self.phi, self.r[2])[0]