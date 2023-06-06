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
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(Rocket("rocket"))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in"})

        self.g_tank.weight_max = 10.0
