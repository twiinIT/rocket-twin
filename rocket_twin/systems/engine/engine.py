from cosapp.base import System


class Engine(System):
    """Simple model of an engine.

    Inputs
    ------
    force_command: float,
        External control, which inputs the % of the maximum force the engine outputs

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

        self.add_inward("force_max", 100.0, desc="Maximum engine force", unit="N")
        self.add_inward(
            "force_command", 1.0, desc="Ratio of command force to maximum force", unit=""
        )

        self.add_outward("weight", 1.0, desc="weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of Gravity", unit="m")
        self.add_outward("force", 1.0, desc="Thrust force", unit="N")

    def compute(self):

        self.force = self.force_max * self.force_command
