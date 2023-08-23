from cosapp.base import System


class ControllerCoSApp(System):
    """System which allows command through CoSApp sequences.

    Inputs
    ------

    Outputs
    ------
    'w' float,
        command flow
    """

    def setup(self):

        self.add_inward("is_on", 0, desc="Whether the fuel flow is allowed or not")

        self.add_outward("w", 1., desc="Ratio of command fuel flow to maximum flow", unit="")

    def compute(self):

        self.w = self.is_on