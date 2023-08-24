from cosapp.base import System


class RocketControllerCoSApp(System):
    """System which allows rocket command through CoSApp sequences.

    Inputs
    ------
    n_stages: int,
        rocket's number of stages
    weight_prop_i: float,
        i-th stage fuel weight

    Outputs
    ------
    is_on_i: float,
        whether the i-th stage controller is active or not
    """

    def setup(self, n_stages):

        self.add_inward("n_stages", n_stages, desc="number of stages")
        self.add_inward("stage", 1, desc="Current active stage")
        self.add_inward("flying", False, desc="Whether the rocket is flying or not")

        for i in range(1, n_stages + 1):
            self.add_inward(f"weight_prop_{i}", 0.0, desc=f"Stage {i} propellant weight", unit="kg")
            self.add_outward(f"is_on_{i}", False, desc=f"Whether the stage {i} is on or not")

        self.add_event("drop", trigger="weight_prop_1 == 0.")

    def transition(self):

        if self.drop.present:
            if self.stage < self.n_stages:
                self[f"is_on_{self.stage}"] = False
                self.stage += 1
                self[f"is_on_{self.stage}"] = True
                self.drop.trigger = f"weight_prop_{self.stage} == 0."
            else:
                self[f"is_on_{self.stage}"] = False
