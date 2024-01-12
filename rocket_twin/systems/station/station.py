from cosapp.base import System

from rocket_twin.systems import Pipe, Rocket, StationControllerCoSApp, Tank


class Station(System):
    """A space station composed by a rocket, a tank, a pipe connecting them and a controller.

    Inputs
    ------
    n_stages: int,
        how many stages are present in the rocket
    fueling: boolean,
        whether the rocket is in the fueling phase
    time_int [s]: float,
        interval between fueling end and launch
    time_lnc [s]: float,
        rocket launch time

    Outputs
    ------
    """

    def setup(self, n_stages=1):

        self.add_inward("n_stages", n_stages, desc="Number of stages")
        self.add_outward("stage", 1, desc="Current stage")

        self.add_inward("fueling", True, desc="Whether the rocket is fueling or not")
        self.add_inward("time_int", 5.0, desc="Interval between fueling end and launch", unit="s")
        self.add_inward("time_lnc", 100000.0, desc="Launch time", unit="s")

        self.add_child(StationControllerCoSApp("controller"), pulling=["fueling"])
        self.add_child(Tank("g_tank"))
        self.add_child(Pipe("pipe"))
        self.add_child(
            Rocket("rocket", n_stages=n_stages), pulling=["a","v", "pos"]
        )  # pulling acceleration and position (from ground to station to rocket to dynamics))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"w_out": "w_in_1"})

        self.connect(self.controller.outwards, self.g_tank.inwards, {"w": "w_command"})

        self.g_tank.geom.height = 2.0

        self.add_event("launch", trigger="t == time_lnc")

    def transition(self):

        for i in range(1, self.n_stages + 1):
            if self.rocket[f"stage_{i}"].controller.full.present:
                if self.stage < self.n_stages:
                    self.pop_child("pipe")
                    self.add_child(Pipe("pipe"), execution_index=2)

                    self.connect(self.g_tank.outwards, self.pipe.inwards, {"w_out": "w_in"})
                    self.connect(
                        self.pipe.outwards, self.rocket.inwards, {"w_out": f"w_in_{self.stage + 1}"}
                    )

                    self.rocket[f"w_in_{self.stage}"] = 0.0
                    self.stage += 1
                else:
                    self.time_lnc = self.time + self.time_int
                    self.fueling = False
                    self.stage = 1

        if self.launch.present:
            self.rocket.flying = True
            self.rocket.controller.is_on_1 = True
