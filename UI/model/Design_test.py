import numpy as np
from cosapp.base import System
from cosapp.drivers import NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.tools import problem_viewer


class Ball(System):
    def setup(self):
        self.add_child(Dynamics("Dyn"))
        self.add_child(Kinematics("Kin"))

        self.connect(self.Dyn, self.Kin, ["a"])


class Dynamics(System):
    def setup(self):
        self.add_inward("a0", 2.0, desc="Acceleration", unit="m/s**2")
        self.add_outward("a", 0.0, desc="Ball Acceleration", unit="m/s**2")

    def compute(self):
        self.a = self.a0


class Kinematics(System):
    def setup(self):
        self.add_inward("a", 0.0, desc="Ball Acceleration", unit="m/s**2")

        self.add_transient("v", der="a", desc="Ball Velocity")
        self.add_transient("r", der="v", desc="Ball Position")
