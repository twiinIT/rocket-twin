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

        self.add_inward('n_stages', n_stages, desc="Number of stages")
        self.add_outward_modevar('stage', 1, desc="Current stage")

        self.add_child(ControllerCoSApp("controller"))
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(Rocket("rocket", n_stages=n_stages))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in_1"})

        self.connect(self.controller.outwards, self.g_tank.inwards, {"w": "w_command"})

        self.g_tank.geom.height = 2.0

        self.add_event("stage_full", trigger="rocket.weight_prop_1 == rocket.weight_max_1")
        self.add_event("stage_empty", trigger="rocket.weight_prop_1 == 0.")

    def transition(self):

        if self.stage_full.present:
            if self.stage < self.n_stages:
                self.stage += 1

                self.pop_child('pipe')
                self.add_child(Pipe('pipe'), execution_index=2)
                #self.exec_order = ["controller", "g_tank", "pipe", "rocket"]

                self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
                self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": f"w_in_{self.stage}"})

                self.rocket[f'w_in_{self.stage - 1}'] = 0.
                self.stage_full.trigger = f"rocket.weight_prop_{self.stage} == rocket.weight_max_{self.stage}"
            else:
                self.controller.w_temp = 0.
                self.rocket[f'w_in_{self.stage}'] = 0.
                self.stage = 1

        if self.stage_empty.present:
            if self.stage < self.n_stages:
                stage = self.rocket.pop_child(f"stage_{self.stage}")
                self.rocket.add_child(stage, execution_index=self.stage - 1)
                self.rocket[f'stage_{self.stage}'].controller.w_temp = 0.
                self.rocket.geom[f'stage_{self.stage}'] = GProp_GProps()

                self.stage += 1
                self.stage_empty.trigger = f"rocket.weight_prop_{self.stage} == 0."
                self.rocket.Takeoff.trigger = "dyn.a == -10000000"
                self.rocket[f'stage_{self.stage}'].controller.w_temp = 1.
            else:
                self.rocket[f'stage_{self.stage}'].controller.w_temp = 0.

