import numpy as np
from cosapp.base import System
from Ports import VelPort


class AeroForces(System):
    def setup(self):
        self.add_inward("v_cpa", np.zeros(3), desc="CPA velocity", unit="m/s")

        self.add_inward(
            "Aeroforces_ang", np.zeros(3), desc="Computing artefact, don't worry"
        )

        # Coefficients inwards
        self.add_inward("Cd", 0.0, desc="Drag coefficient", unit="")
        self.add_inward("N", 0.0, desc="Normal force", unit="")
        self.add_inward("S_ref", 1.0, desc="Reference Surface", unit="m**2")

        # Atmosphere
        self.add_inward("rho", 1.292, unit="kg/m**3")

        # Wind
        self.add_input(VelPort, "v_wind")

        self.add_outward("F", np.zeros(3), desc="Aerodynamic Forces", unit="N")

        # Parachute
        self.add_inward("ParaDep", False, desc="Parachute Deployed", unit="")

    def compute(self):
        if self.ParaDep:
            return

        self.v_cpa -= self.v_wind.val

        Fd = 0.5 * self.rho * np.linalg.norm(self.v_cpa) ** 2 * self.S_ref * self.Cd
        Fn = self.N

        a = np.arctan2(self.v_cpa[2], self.v_cpa[1])

        Fnz = -Fn * np.sin(a)
        Fny = -Fn * np.cos(a)

        self.F = [-Fd, Fny, Fnz]
