from cosapp.base import System


class StageControllerCoSApp(System):
    """System which allows stage command through CoSApp sequences.

    Inputs
    ------
    is_on: int,
        whether the stage is on or not
    weight_prop: float,
        stage fuel weight
    weight_max: float,
        stage maximum fuel weight

    Outputs
    ------
    w: float,
        command flux
    """

    def setup(self):

        self.add_inward("weight_prop", 0.0, desc="Stage propellant weight", unit="kg")
        self.add_inward("weight_max", 1.0, desc="Stage maximum propellant weight", unit="kg")
        self.add_inward("is_on", False, desc="Whether the stage is on or not")

        self.add_outward("w", 1.0, desc="Command flow", unit="")

        self.add_event("full", trigger="weight_prop == weight_max")

    def compute(self):

        self.w = self.is_on
