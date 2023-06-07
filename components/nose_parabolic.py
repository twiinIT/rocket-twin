from cosapp.base import System


class NoseParabolic(System):
    # Nose given by the function x**2 + y**2 = a*z with a = Rp**2/Lp
    def setup(self):
        # Paraboloid Geometry parameters
        self.add_inward("Lp", 1.0, desc="Paraboloid height", unit="m")
        self.add_inward("Rp", 1.0, desc="Paraboloid maximum radius", unit="m")

        # Paraboloid outputs
        self.add_outward(
            "Cna", 2.0, desc="Paraboloid normal force coefficient slope", unit=""
        )
        self.add_outward("Cd", 0.0, desc="Paraboloid drag coefficient", unit="")
        self.add_outward("Xcp", 1.0, desc="Paraboloid center of pressure", unit="m")
        self.add_outward("Xcg", 1.0, desc="Paraboloid center of gravity", unit="m")

    def compute(self):
        self.Xcp = self.Lp / 2
        self.Xcg = 2 * self.Lp / 3
