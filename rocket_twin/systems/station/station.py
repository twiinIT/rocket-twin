from cosapp.base import System

from rocket_twin.systems import ControllerCoSApp, Pipe, Rocket, Tank


class Station(System):
    """A space station composed by a rocket, a tank, a pipe connecting them and a controller.

    Inputs
    ------

    Outputs
    ------
    """

    def setup(self):
        self.add_child(ControllerCoSApp("controller"))
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(Rocket("rocket"))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in"})

        self.connect(self.controller.outwards, self.g_tank.inwards, {"w": "w_command"})

        self.g_tank.weight_max = 10.0
