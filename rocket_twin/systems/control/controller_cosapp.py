from cosapp.base import System


class ControllerCoSApp(System):
    """System which allows command through CoSApp sequences.

    Inputs
    ------
    is_on: float,
        whether the system is active or not

    Outputs
    ------
    'w': float,
        command flow
    """

    def setup(self):

        self.add_inward("is_on", True, desc="Whether the fuel flow is allowed or not")

        self.add_outward("w", 1.0, desc="Ratio of command fuel flow to maximum flow", unit="")

    def compute(self):

        self.w = self.is_on
        print(self.parent.name, self.time)
