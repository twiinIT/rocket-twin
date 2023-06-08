from cosapp.base import System
import numpy as np

class NoseOgive(System):
    def setup(self):
        # Cone Geometry parameters
        self.add_inward("Lo", 1.0, desc="Ogive Height", unit="m")
        self.add_inward("Ro", 1.0, desc="Ogive Radius", unit="m")
        self.add_inward("rho", 1.0, desc="Ogive material density", unit="kg/m**3")

        # Cone outputs
        self.add_outward(
            "Cna", 2.0, desc="Ogive normal force coefficient slope", unit=""
        )
        self.add_outward("Cd", 0.0, desc="Ogive drag coefficient", unit="")
        self.add_outward("Xcp", 1.0, desc="Ogive center of pressure", unit="m")
        self.add_outward("Xcg", 1.0, desc="Ogive center of gravity", unit="m")
        self.add_outward("m", 1.0, desc="Ogive mass", unit='kg')
        self.add_outward("I", np.zeros(3), desc="Ogive principal moments of inertia", unit='kg*m**2')

    def compute(self):
        self.Xcp = 0.466 * self.Lc

        lbda = self.Lo / self.Ro
        f = ((lbda) ** 2 + 1) / 2

        V = (
            np.pi(
                (f**2 - (lbda**2) / 3) * lbda - f**2(f - 1) * np.arcsin(lbda / f)
            )
            * self.Ro**3
        )  # Ogive Volume

        self.Xcg = (
            np.pi
            * (
                (-2 / 3) * (f - 1) * (f**3 - (f - 1) ** 3)
                + (1 / 2) * (f**2 + (f - 1) ** 2) * lbda**2
                - lbda**4 / 4
            )
            * self.Ro**4
            / V
        )

        Iz = (self.rho * self.Ro**5 * np.pi / 2) * (
            (f**4 + (9 / 2) * f * (f - 1) ** 2 - 2 * (f - 1) ** 4) * lbda
            - ((2 / 3) * f**2 + 2 * (f - 1) ** 2) * lbda**3
            + lbda**5 / 5
            - f**2
            * (f - 1)
            * ((3 / 2) * f**2 + 2 * (f - 1) ** 2)
            * np.arcsin(lbda / f)
        )

        Ix = (self.rho * self.Ro**5 * np.pi / 4) * (
            f**2 * (f**2 + (7 / 2) * (f - 1) ** 2) * lbda
            + lbda**5 / 15
            - f**2
            * (f - 1) * ((5 / 2) * f**2 + 2 * (f - 1) ** 2)
            * np.arcsin(lbda / f)
        )

        Ix -= (self.Xcg/self.Ro)**2*(self.rho*self.Ro**2*V)

        self.I = np.array([Ix,Ix,Iz])
        self.m = self.rho*V
