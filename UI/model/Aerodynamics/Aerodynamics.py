import numpy as np
from aerodynamics.aeroforces import AeroForces
from aerodynamics.coefficients import Coefficients
from aerodynamics.moments import Moments
from cosapp.base import System
from ports import VelPort


class Aerodynamics(System):
    def setup(self):
        # System orientation
        self.add_inward("Aero_ang", np.zeros(3), desc="Rocket Euler Angles")

        # Geometry
        self.add_inward("m", desc="mass", unit="kg")
        self.add_inward("CG", desc="Rocket center of gravity", unit="m")

        self.add_input(VelPort, "v_wind")

        self.add_outward("F", np.zeros(3), desc="Aerodynamics Forces", unit="N")
        self.add_outward("Ma", np.zeros(3), desc="Aerodynamics Moments", unit="N*m")

        # Parachute
        self.add_inward("ParaDep", False, desc="Parachute Deployed", unit="")

        self.add_child(
            AeroForces("Aeroforces"), pulling=["v_cpa", "F", "rho", "v_wind", "ParaDep"]
        )
        self.add_child(
            Coefficients("Coefs"),
            pulling=["v_cpa", "l", "rho", "v_wind", "av", "ParaDep"],
        )
        self.add_child(Moments("Moments"), pulling=["Ma", "ParaDep", "CG"])

        self.connect(self.Coefs, self.Aeroforces, ["Cd", "N", "S_ref"])
        self.connect(self.Coefs, self.Moments, ["Xcp", "l", "M", "Mroll"])
        self.connect(self.Aeroforces, self.Moments, ["F"])

        self.exec_order = ["Coefs", "Aeroforces", "Moments"]
