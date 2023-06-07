from cosapp.base import System


class NoseCone(System):
    def setup(self):
        # Cone Geometry parameters
        self.add_inward("Lc", 1.0, desc="Cone height", unit="m")
        self.add_inward("Rc", 1.0, desc="Cone radius", unit="m")

        # Cone outputs
        self.add_outward(
            "Cna", 2.0, desc="Cone normal force coefficient slope", unit=""
        )
        self.add_outward("Cd", 1.0, desc="Cone drag coefficient", unit="")
        self.add_outward("Xcp", 1.0, desc="Cone center of pressure", unit="m")
        self.add_outward("Xcg", 1.0, desc="Cone center of gravity", unit="m")

    def compute(self):
        self.Xcp = 2 * self.Lc / 3
        self.Xcg = 3 * self.Lc / 4
        self.Cd = 0.8 * (self.Rc / (self.Rc**2 + self.Lc**2) ** 0.5)
