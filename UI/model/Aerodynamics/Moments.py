import numpy as np
from cosapp.base import System


class Moments(System):
    def setup(self):
        # Force inward
        self.add_inward("F", np.zeros(3), desc="Aerodynamic Forces", unit="N")

        # Moments inwards
        self.add_inward("M", 0.0, desc="Pitch moment")
        self.add_inward("Mroll", 0.0, desc="Roll  moment")

        # Geometry inwards
        self.add_inward("Xcp", 0.0, desc="CPA position from the rocket top", unit="m")
        self.add_inward("l", desc="Rocket length", unit="m")
        self.add_inward("CG", desc="Center of Gravity", unit="m")

        # Outward
        self.add_outward("Ma", np.zeros(3), desc="Aerodynamic Moments", unit="N*m")

        # Parachute
        self.add_inward("ParaDep", False, desc="Parachute Deployed", unit="")

    def compute(self):
        if self.ParaDep:
            return

        # Lever arm technique
        OM = np.array([self.CG - self.Xcp, 0, 0])
        self.Ma = np.cross(OM, self.F)
        self.Ma[0] += self.Mroll
