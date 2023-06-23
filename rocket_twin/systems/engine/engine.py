from cosapp.base import System


class Engine(System):
    def setup(self):
        self.add_outward("weight", 1.0, desc="weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of Gravity", unit="m")
        self.add_outward("force", 1.0, desc="Thrust force", unit="N")

    def compute(self):
        self.force = 100.0
        self.cg = 1.0
