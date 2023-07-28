from cosapp.base import System

from rocket_twin.systems import ControllerCoSApp, Pipe, Rocket, Tank


class Station(System):
    """A space station composed by a rocket, a tank, a pipe connecting them and a controller.

    Inputs
    ------

    Outputs
    ------
    """

    def setup(self, n_stages=1):
        self.add_child(ControllerCoSApp("controller"))
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(Rocket("rocket", n_stages=n_stages))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in"})

        self.connect(self.controller.outwards, self.g_tank.inwards, {"w": "w_command"})

        self.g_tank.weight_max = 10.0

        self.add_outward_modevar("low_stage", 1, desc="Rocket's lowest stage")
        self.add_event("Separation", trigger="rocket.stage_1.weight_p == 0.")

        self.add_transient('a_bug', der='time')


    def transition(self):

        if self.Separation.present and len(self.rocket.children) > 2:
            print("TRANSITION")
            stage = "disc_stage_" + str(self.low_stage)
            self.split_rocket(self.rocket, "rocket", stage, 1)
            self.low_stage += 1
            self.rocket.stage_1.controller.w_temp = 1.

    def add_rocket(self, name, n_stages):

        self.add_child(Rocket(name=name, n_stages=n_stages))

    def split_rocket(self, rocket, name_1, name_2, n_stages):

        total_stages = len(rocket.children) - 1
        self.pop_child(rocket.name)
        self.add_child(Rocket(name_1, n_stages=total_stages - n_stages, full=True), pulling=['a_bug'])
        self.add_child(Rocket(name_2, n_stages=n_stages), pulling=['a_bug'])
