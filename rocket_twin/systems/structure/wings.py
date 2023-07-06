from cosapp.base import System

class Wings(System):
    """Model of the wings of a rocket.

    Inputs
    ------

    Outputs
    ------
    weight [kg]: float,
        wings weight
    cg [m]: float,
        wings center of gravity
    """

    def setup(self):

        self.add_outward('weight', 0., desc="Weight", unit='kg')
        self.add_outward('cg', 0., desc="Center of gravity", unit='m')