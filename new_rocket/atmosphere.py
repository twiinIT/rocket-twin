from cosapp.base import System

from density import Density
from pressure import Pressure

class Atmosphere(System):

    def setup(self):

        self.add_child(Density('dens'), pulling=['r', 'rho'])
        self.add_child(Pressure('pres'), pulling=['r'])