from cosapp.base import System


class CosappController(System):
    """System which allows command through CoSApp sequences.

    Inputs
    ------

    Outputs
    ------
    'f': float,
        command force
    'wr': float,
        command flow
    'wg' float,
        command flow
    """

    def setup(self):

        self.add_inward("f_temp", 0.0, desc="Ratio of command force to maximum force", unit="")
        self.add_inward("wr_temp", 0.0, desc="Ratio of command fuel flow to maximum flow", unit="")
        self.add_inward("wg_temp", 0.0, desc="Ratio of command fuel flow to maximum flow", unit="")

        self.add_outward("f", 0.0, desc="Ratio of command force to maximum force", unit="")
        self.add_outward("wr", 0.0, desc="Ratio of command fuel flow to maximum flow", unit="")
        self.add_outward("wg", 0.0, desc="Ratio of command fuel flow to maximum flow", unit="")

    def compute(self):

        self.f = self.f_temp
        self.wr = self.wr_temp
        self.wg = self.wg_temp
