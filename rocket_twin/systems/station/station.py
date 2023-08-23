from cosapp.base import System
from OCC.Core.GProp import GProp_GProps

from rocket_twin.systems import ControllerCoSApp, Pipe, Rocket, Tank


class Station(System):
    """A space station composed by a rocket, a tank, a pipe connecting them and a controller.

    Inputs
    ------

    Outputs
    ------
    """

    def setup(self, n_stages=1):

        self.add_inward("n_stages", n_stages, desc="Number of stages")
        self.add_outward("stage", 1, desc="Current stage")

        self.add_child(ControllerCoSApp("controller"))
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(Rocket("rocket", n_stages=n_stages))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in_1"})

        self.connect(self.rocket.outwards, self.controller.inwards, {'fueling' : 'is_on'})
        self.connect(self.controller.outwards, self.g_tank.inwards, {"w": "w_command"})

        self.g_tank.geom.height = 2.0

    def transition(self):

        if self.rocket.controller.full.present:
            if self.stage < self.n_stages:
                self.pop_child("pipe")
                self.add_child(Pipe("pipe"), execution_index=2)

                self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
                self.connect(
                    self.pipe.outwards, self.rocket.inwards, {"w_out": f"w_in_{self.stage + 1}"}
                )

                self.rocket[f"w_in_{self.stage}"] = 0.0
                self.stage += 1
