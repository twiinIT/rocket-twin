from cosapp.base import System


class Engine(System):
    """Simple model of an engine.

    Inputs
    ------

    Outputs
    ------
    weight [kg]: float,
        weight
    cg [m]: float,
        position of the center of gravity
    force [N]: float,
        thrust force
    """

    def setup(self):
        self.add_outward("weight", 1.0, desc="weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of Gravity", unit="m")
        self.add_outward("force", 1.0, desc="Thrust force", unit="N")

    def compute(self):
        self.force = 100.0
        self.cg = 1.0
