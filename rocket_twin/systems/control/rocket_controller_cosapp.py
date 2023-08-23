from cosapp.base import System


class RocketControllerCoSApp(System):
    """System which allows rocket command through CoSApp sequences.

    Inputs
    ------
    model_path: string,
        the path to the .mo file, if any
    model_name: string,
        the .fmu file name
    n_stages: int,
        rocket's number of stages
    weight_prop_i: float,
        i-th stage fuel weight
    weight_max_i: float,
        i-th stage maximum fuel weight

    Outputs
    ------
    is_on_i: float,
        whether the i-th stage controller is active or not
    fueling: float,
        whether the rocket is in the fueling phase or not
    flying: float,
        whether the rocket is mid-flight or not
    """

    def setup(self, n_stages):

        self.add_inward("n_stages", n_stages, desc="number of stages")
        self.add_inward("stage", 1, desc="Current active stage")

        for i in range(1, n_stages + 1):
            self.add_inward(f"weight_prop_{i}", 0.0, desc=f"Stage {i} propellant weight", unit="kg")
            self.add_inward(
                f"weight_max_{i}", 1.0, desc=f"Stage {i} maximum propellant weight", unit="kg"
            )
            self.add_outward(f"is_on_{i}", 0, desc=f"Whether the stage {i} is on or not")

        self.add_inward("time_int", 5.0, desc="Interval between fueling end and launch", unit="s")
        self.add_inward("time_lnc", 100000.0, desc="Launch time", unit="s")

        self.add_outward("fueling", 1, desc="Whether the rocket is fueling or not")
        self.add_outward("flying", 0, desc="Whether the rocket is flying or not")

        self.add_event("full", trigger="weight_prop_1 == weight_max_1")
        self.add_event("launch", trigger="t == time_lnc")
        self.add_event("drop", trigger="weight_prop_1 == 0.")

    def transition(self):

        if self.full.present:
            if self.stage < self.n_stages:
                self.stage += 1
                self.full.trigger = f"weight_prop_{self.stage} == weight_max_{self.stage}"
            else:
                self.time_lnc = self.time + self.time_int
                self.fueling = 0
                self.stage = 1
        if self.launch.present:
            self.flying = 1
            self.is_on_1 = 1
        if self.drop.present:
            if self.stage < self.n_stages:
                self[f"is_on_{self.stage}"] = 0
                self.stage += 1
                self[f"is_on_{self.stage}"] = 1
                self.drop.trigger = f"weight_prop_{self.stage} == 0."
            else:
                self[f"is_on_{self.stage}"] = 0
