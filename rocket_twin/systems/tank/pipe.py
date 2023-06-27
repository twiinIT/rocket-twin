from cosapp.base import System


class Pipe(System):
    def setup(self):

        self.add_inward("p_in", 0.0, desc="Fuel income rate", unit="kg/s")
        self.add_outward("p_out", 0.0, desc="Fuel exit rate", unit="kg/s")

    def compute(self):
        self.p_out = self.p_in
