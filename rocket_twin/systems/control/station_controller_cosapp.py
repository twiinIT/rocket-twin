from cosapp.base import System


class StationControllerCoSApp(System):
    """System which allows station command through CoSApp sequences.

    Inputs
    ------
    fueling: boolean,
        whether the system is in fueling phase or not

    Outputs
    ------
    w: float,
        command flux
    """

    def setup(self):

        self.add_inward("fueling", False, desc="Whether the system is in the fueling phase or not")

        self.add_outward("w", 1.0, desc="Command flow", unit="")

    def compute(self):

        self.w = self.fueling
