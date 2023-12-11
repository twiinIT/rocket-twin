import numpy as np
from cosapp.base import System


class EnginePerfo(System):
    """Simple model of an engine's thrust force.

    Inputs
    ------
    w_out [kg/s]: float,
        fuel consumption rate

    Outputs
    ------
    force [N]: float,
        thrust force
    """

    def setup(self):

        # Inputs
        self.add_inward("w_out", 0.0, desc="Fuel consumption rate", unit="kg/s")

        # Parameters
        self.add_inward("isp", 20.0, desc="Specific impulsion in vacuum", unit="s")
        self.add_inward("g_0", 10.0, desc="Gravity at Earth's surface", unit="m/s**2")

        self.add_outward("force", np.array([0.0, 0.0, 1.0]), desc="Thrust force", unit="N")

    def compute(self):

        self.force = np.array([0.0, 0.0, self.isp * self.w_out * self.g_0])
