from cosapp.base import System


class Tank(System):
    def setup(self):
        self.add_inward("w_s", 1.0, desc="Structure weight", unit="kg")
        self.add_inward("p_in", 0.0, desc="Fuel income rate", unit="kg/s")
        self.add_inward("p_out", 0.0, desc="Fuel consumption rate", unit="kg/s")
        self.add_inward("w_max", 5.0, desc="Maximum fuel capacity", unit="kg")

        self.add_transient("w_p", der="p_in - p_out", desc="Propellant weight")

        self.add_outward("weight", 1.0, desc="Weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of gravity", unit="m")

    def compute(self):
        self.weight = self.w_s + self.w_p
        self.cg = 3.0
