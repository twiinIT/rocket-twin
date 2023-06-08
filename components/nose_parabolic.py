from cosapp.base import System
import numpy as np


class NoseParabolic(System):
    # Nose given by the function x**2 + y**2 = a*z with a = Rp**2/Lp
    def setup(self):
        # Paraboloid Geometry parameters
        self.add_inward("Lp", 1.0, desc="Paraboloid height", unit="m")
        self.add_inward("Rp", 1.0, desc="Paraboloid maximum radius", unit="m")
        self.add_inward("rho", 1.0, desc="Paraboloid material density", unit="kg/m**3")

        # Paraboloid outputs
        self.add_outward(
            "Cna", 2.0, desc="Paraboloid normal force coefficient slope", unit=""
        )
        self.add_outward("Cd", 0.0, desc="Paraboloid drag coefficient", unit="")
        self.add_outward("Xcp", 1.0, desc="Paraboloid center of pressure", unit="m")
        self.add_outward("Xcg", 1.0, desc="Paraboloid center of gravity", unit="m")
        self.add_outward("m", 1., desc="Paraboloid mass", unit="kg")
        self.add_outward("I", np.zeros(3), desc="Paraboloid principal inertia moments", unit="kg*m**2")

    def compute(self):
        self.Xcp = self.Lp / 2
        self.Xcg = 2 * self.Lp / 3

        a = self.Rp**2/self.Lp
        V = np.pi*a*self.Lp**2/2

        self.m = self.rho * V
        
