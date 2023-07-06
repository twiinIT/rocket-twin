from cosapp.base import System

class Nose(System):
    """Model of a rocket nose.

    Inputs
    ------

    Outputs
    ------
    weight [kg]: float,
        nose weight
    cg [m]: float,
        nose center of gravity
    """

    def setup(self):

        self.add_outward('weight', 0., desc="Weight", unit='kg')
        self.add_outward('cg', 0., desc="Center of gravity", unit='m')