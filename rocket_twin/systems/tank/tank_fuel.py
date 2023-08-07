from cosapp.base import System

class TankFuel(System):
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
    """

    def setup(self):

        # Fuel
        self.add_inward("weight_s", 1.0, desc="Structure weight", unit="kg")
        self.add_inward("weight_max", 5.0, desc="Maximum fuel capacity", unit="kg")

        # Flux control
        self.add_inward("w_out_max", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_inward("w_command", 1.0, desc="Fuel output control variable", unit="")

        # Inputs
        self.add_inward("w_in", 0.0, desc="Fuel income rate", unit="kg/s")

        # Outputs
        self.add_outward("w_out", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_outward("weight", 1., desc="Total weight", unit="kg")

        # Transient
        self.add_transient("weight_p", der="w_in - w_out", desc="Propellant weight")

    def compute(self):

        self.w_out = self.w_out_max * self.w_command
        self.weight = self.weight_s + self.weight_p