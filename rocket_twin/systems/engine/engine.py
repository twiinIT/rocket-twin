from cosapp.base import System


class Engine(System):
    """Simple model of an engine.

    Inputs
    ------
    force_command: float,
        external control, which inputs the % of the maximum force the engine outputs
    w_out [kg/s]: float,
        rate of fuel consumption

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

        #self.add_inward("force_max", 100.0, desc="Maximum engine force", unit="N")
        self.add_inward(
            "force_command", 1.0, desc="Ratio of command force to maximum force", unit=""
        )
        self.add_inward("isp", 100., desc="Specific impulsion in vacuum", unit='s')
        self.add_inward("w_out", 0., desc="Fuel consumption rate", unit='kg/s')
        self.add_inward("g_0", 9.80665, desc="Gravity at Earth's surface", unit='m/s**2')

        self.add_outward("weight", 1.0, desc="weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of Gravity", unit="m")
        self.add_outward("force", 1.0, desc="Thrust force", unit="N")

    def compute(self):

        self.force = self.isp * self.g_0 * self.w_out * self.force_command
