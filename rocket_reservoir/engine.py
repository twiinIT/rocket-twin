from cosapp.base import System

class Engine(System):

    def setup(self):

        self.add_outward('m', 1., desc="Mass", unit='kg')
        self.add_outward('xcg', 1., desc="Center of Gravity", unit='m')
        self.add_outward('force', 1., desc="Thrust force", unit='N')

    def compute(self):

        self.force = 100.