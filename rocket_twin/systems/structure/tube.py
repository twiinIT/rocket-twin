from cosapp.base import System

class Tube(System):
    """Model of a rocket tube.

    Inputs
    ------

    Outputs
    ------
    weight [kg]: float,
        tube weight
    cg [m]: float,
        tube center of gravity
    """

    def setup(self):

        self.add_outward('weight', 0., desc="Weight", unit='kg')
        self.add_outward('cg', 0., desc="Center of gravity", unit='m')