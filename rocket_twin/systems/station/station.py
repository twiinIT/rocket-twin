from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem

from rocket_twin.systems import Clock, Pipe, Rocket, Tank
from rocket_twin.utils import create_FMU


class Station(System):
    """A space station composed by a rocket, a tank and a pipe connecting them.

    Inputs
    ------
    fmu_path: string,
        the path to the .fmu file, if there is any

    Outputs
    ------
    """

    def setup(self, model_path=None, model_name=None):
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(Rocket("rocket"))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in"})

        if model_path is not None:
            self.add_child(Clock("clock"))
            fmu_path = create_FMU(model_path, model_name)
            self.add_child(FMUSystem("controller", fmu_path=fmu_path))
            self.connect(self.clock.outwards, self.controller.inwards, {"time_var": "ti"})
            self.connect(self.controller.outwards, self.g_tank.inwards, {"wg": "w_command"})
            self.connect(
                self.controller.outwards,
                self.rocket.inwards,
                {"wr": "w_command", "f": "force_command"},
            )

            self.exec_order = ["clock", "controller", "g_tank", "pipe", "rocket"]

        self.g_tank.weight_max = 10.0
