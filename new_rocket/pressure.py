from cosapp.base import System

class Pressure(System):

    def setup(self):

        self.add_inward('x')