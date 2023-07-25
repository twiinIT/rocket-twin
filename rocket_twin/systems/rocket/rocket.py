from cosapp.base import System
from cosapp.utils import get_state

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
            self.add_child(Stage(f"stage_{i}"))
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

        self.stage_1.controller.w_temp = 1.

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
        self.add_outward_modevar("stage", 1, desc="Rocket's current stage", unit='')

        self.add_event("Takeoff", trigger="dyn.a > 0")
        self.add_event("Removal", trigger="stage_1.weight_p == 0.")


    def compute(self):
        self.a *= self.flying
        print('massa 1: ', self.stage_1.weight_p)
        print('tempo: ', self.time)

    def transition(self):

        if self.Takeoff.present:
            self.flying = True
        if self.Removal.present:
            print(f"REMOVAL {self.stage}")

            self.dyn.inwards[f'thrust_{self.stage}'] = 0.
            self.dyn.inwards[f'weight_{self.stage}'] = 0.
            self.dyn.inwards[f'center_{self.stage}'] = 0.

            self.stage += 1
            cur_stage = list(self.children.values())[1]
            cur_stage.controller.w_temp = 1.

            self.Removal.trigger = f"stage_{self.stage}.weight_p == 0."
            self.pop_child(list(self.children.keys())[0])
            


