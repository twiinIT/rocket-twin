from cosapp.base import System

from rocket_twin.systems import Dynamics
from rocket_twin.systems.rocket import Stage


class Rocket(System):
    """A simple model of a rocket.

    Inputs
    ------
    n_stages: int,
        how many stages the rocket has
    flying: boolean,
        whether the rocket is already flying or still on ground

    Outputs
    ------
    """

    def setup(self, n_stages=1):

        forces, weights, centers = ([None] * n_stages for i in range(3))

        for i in range(1, n_stages + 1):
            self.add_child(Stage(f"stage_{i}"), pulling=["w_in"])
            forces[i - 1] = f"thrust_{i}"
            weights[i - 1] = f"weight_{i}"
            centers[i - 1] = f"center_{i}"

        self.add_child(
            Dynamics(
                "dyn",
                forces=forces,
                weights=weights,
                centers=centers,
            ),
            pulling=["a"],
        )

        stages = list(self.children.values())

        for i in range(0, len(stages) - 1):
            self.connect(
                stages[i].outwards,
                self.dyn.inwards,
                {"force": f"thrust_{i + 1}", "weight": f"weight_{i + 1}", "cg": f"center_{i + 1}"},
            )

        self.add_inward_modevar(
            "flying", False, desc="Whether the rocket is flying or not", unit=""
        )
        self.add_outward_modevar("stage", 1, desc="Rocket's current stage", unit="")

        self.add_event("Takeoff", trigger="dyn.a > 0")
        self.add_event("Removal", trigger="stage_1.weight_p == 0.")

    def compute(self):
        self.a *= self.flying

    def transition(self):

        if self.Takeoff.present:
            self.flying = True
        if self.Removal.present:
            print(f"REMOVAL {self.stage}")

            cur_stage = list(self.children.values())[self.stage - 1]
            next_stage = list(self.children.values())[self.stage]
            if next_stage.name != "dyn":
                cur_stage.connected = False
                next_stage.controller.w_temp = 1.0
                self.Removal.trigger = f"stage_{self.stage}.weight_p == 0."
                self.stage += 1
