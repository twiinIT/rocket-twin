from cosapp.base import System
from pyatmos import coesa76
import numpy as np

class Pressure(System):

    def setup(self):

        self.add_inward('r', np.zeros(3), desc="Rocket position", unit='m')

        self.add_outward('P', 1., desc="Atmospheric pressure at rocket's height", unit='Pa')

    def compute(self):

        self.P = coesa76([self.r[2]/1000]).P