from cosapp.base import System
import numpy as np


class NoseCone(System):
    def setup(self):
        # Cone Geometry parameters
        self.add_inward("Lc", 1.0, desc="Cone height", unit="m")
        self.add_inward("Rc", 1.0, desc="Cone radius", unit="m")
        self.add_inward("rho", 1.0, desc="Cone material density", unit="kg/m**3")

        # Cone outputs
        self.add_outward(
            "Cna", 2.0, desc="Cone normal force coefficient slope", unit=""
        )
        self.add_outward("Cd", 1.0, desc="Cone drag coefficient", unit="")
        self.add_outward("Xcp", 1.0, desc="Cone center of pressure", unit="m")
        self.add_outward("Xcg", 1.0, desc="Cone center of gravity", unit="m")
        self.add_outward("m", 1., desc="Cone mass", unit="kg")
        self.add_outward("I", np.zeros(3), desc="Cone principal inertia moments", unit="kg*m**2")

    def compute(self):
        self.Xcp = 2 * self.Lc / 3
        self.Xcg = 3 * self.Lc / 4
        self.Cd = 0.8 * (self.Rc / (self.Rc**2 + self.Lc**2) ** 0.5)

        V = self.Lc*np.pi*self.Rc**2/3

        self.m = self.rho * V

        Iz = (3/10)*self.m*self.Rc**2
        Ix = (3*self.m/20)*(self.Rc**2 + self.Lc**2/4)

        self.I = np.array([Ix,Ix,Iz])


