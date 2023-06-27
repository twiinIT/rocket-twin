from cosapp.base import System


class Tank(System):
    def setup(self):

        #Geometry
        self.add_inward("w_s", 1.0, desc="Structure weight", unit="kg")
        self.add_inward("w_max", 5.0, desc="Maximum fuel capacity", unit="kg")

        #Inputs
        self.add_inward("p_in", 0.0, desc="Fuel income rate", unit="kg/s")

        #Flux control
        self.add_inward('flux', 0., desc="Fuel output rate", unit='kg/s')

        #Transient
        self.add_outward("dp_dt", 0., desc="Fuel mass rate of change", unit="kg/s")
        self.add_transient("w_p", der="dp_dt", desc="Propellant weight")

        #Outputs
        self.add_outward("weight", 1.0, desc="Weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of gravity", unit="m")
        self.add_outward("p_out", 0.0, desc="Fuel output rate", unit="kg/s")

    def compute(self):
        self.p_out = self.flux
        self.dp_dt = self.p_in - self.p_out
        self.weight = self.w_s + self.w_p
        self.cg = 3.0
