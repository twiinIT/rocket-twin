from cosapp.base import System
from pyatmos import coesa76
import numpy as np

class Density(System):

    def setup(self):

        self.add_inward('r', np.zeros(3), desc="Rocket position", unit='m')

        self.add_outward('rho', 1., desc="Air density at rocket's height", unit='kg/m**3')

    def compute(self):

        self.rho = coesa76([self.r[2]/1000]).rho