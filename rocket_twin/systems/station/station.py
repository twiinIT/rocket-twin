from cosapp.base import System

from rocket_twin.systems import Pipe, Rocket, Tank


class Station(System):
    """A space station composed by a rocket, a tank and a pipe connecting them.

    Inputs
    ------

    Outputs
    ------
    """

    def setup(self):
        self.add_child(Rocket("rocket"))
        self.add_child(Pipe("pipe"))
        self.add_child(Tank("g_tank"))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in"})

        self.g_tank.weight_max = 10.0
        self.rocket.tank.weight_p = 0.0

        self.exec_order = ["pipe", "g_tank", "rocket"]

        # Design methods
        dm = self.add_design_method("start")
        dm.add_unknown("g_tank.weight_p")
        dm.add_equation("g_tank.weight_p == g_tank.weight_max")
