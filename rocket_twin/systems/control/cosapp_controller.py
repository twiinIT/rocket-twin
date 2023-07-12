from cosapp.base import System


class CosappController(System):
    """System which allows command through CoSApp sequences.

    Inputs
    ------

    Outputs
    ------
    'w' float,
        command flow
    """

    def setup(self):

        self.add_inward("w_temp", 0.0, desc="Ratio of command fuel flow to maximum flow", unit="")

        self.add_outward("w", 0.0, desc="Ratio of command fuel flow to maximum flow", unit="")

    def compute(self):

        self.w = self.w_temp
