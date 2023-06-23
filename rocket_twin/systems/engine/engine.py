from cosapp.base import System

class Engine(System):

    def setup(self):

        self.add_outward('weight', 1., desc="weight", unit='kg')
        self.add_outward('cg', 1., desc="Center of Gravity", unit='m')
        self.add_outward('force', 1., desc="Thrust force", unit='N')

    def compute(self):

        self.force = 100.
        self.cg = 1.