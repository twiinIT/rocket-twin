from cosapp.base import System


class Pipe(System):
    def setup(self):

        self.add_inward("w_in", 0.0, desc="Fuel income rate", unit="kg/s")
        self.add_outward("w_out", 0.0, desc="Fuel exit rate", unit="kg/s")

    def compute(self):
        self.w_out = self.w_in
