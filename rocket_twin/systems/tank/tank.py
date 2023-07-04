from cosapp.base import System


class Tank(System):
    """A simple model of a fuel tank.

    Inputs
    ------
    w_in [kg/s]: float,
        mass flow of fuel entering the tank
    w_command: float,
        fuel exit flux control. 0 means tank exit fully closed, 1 means fully open

    Outputs
    ------
    w_out [kg/s]: float,
        mass flow of fuel exiting the tank
    weight [kg]: float,
        weight
    cg [m]: float,
        center of gravity
    """

    def setup(self):

        # Geometry
        self.add_inward("weight_s", 1.0, desc="Structure weight", unit="kg")
        self.add_inward("weight_max", 5.0, desc="Maximum fuel capacity", unit="kg")

        # Inputs
        self.add_inward("w_in", 0.0, desc="Fuel income rate", unit="kg/s")

        # Flux control
        self.add_inward("w_out_temp", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_inward("w_command", 1.0, desc="Fuel output control variable", unit="")

        # Transient
        self.add_outward("dw_dt", 0.0, desc="Fuel mass rate of change", unit="kg/s")
        self.add_transient("weight_p", der="dw_dt", desc="Propellant weight")

        # Outputs
        self.add_outward("weight", 1.0, desc="Weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of gravity", unit="m")
        self.add_outward("w_out", 0.0, desc="Fuel output rate", unit="kg/s")

    def compute(self):
        self.w_out = self.w_out_temp * self.w_command
        self.dw_dt = self.w_in - self.w_out
        self.weight = self.weight_s + self.weight_p
