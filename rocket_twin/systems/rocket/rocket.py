from cosapp.base import System

from rocket_twin.systems import Dynamics
from rocket_twin.systems.rocket import OCCGeometry, Stage


class Rocket(System):
    """A simple model of a rocket.

    Inputs
    ------
    flying: boolean,
        whether the rocket is already flying or still on ground

    Outputs
    ------
    """

    def setup(self, n_stages=1):

        shapes, properties, forces = ([None] * n_stages for i in range(3))

        for i in range(1, n_stages + 1):
            nose = False
            wings = False
            if i == 1:
                wings = True
            if i == n_stages:
                nose = True

            self.add_child(
                Stage(f"stage_{i}", nose=nose, wings=wings),
                pulling={
                    "w_in": f"w_in_{i}",
                    "weight_max": f"weight_max_{i}",
                    "weight_prop": f"weight_prop_{i}",
                },
            )
            shapes[i - 1] = f"stage_{i}_s"
            properties[i - 1] = f"stage_{i}"
            forces[i - 1] = f"thrust_{i}"

        self.add_child(OCCGeometry("geom", shapes=shapes, properties=properties))
        self.add_child(Dynamics("dyn", forces=forces, weights=["weight_rocket"]), pulling=["a"])

        for i in range(1, n_stages + 1):
            self.connect(self[f"stage_{i}"].outwards, self.geom.inwards, {"props": f"stage_{i}"})
            self.connect(self[f"stage_{i}"].outwards, self.dyn.inwards, {"thrust": f"thrust_{i}"})

        self.connect(self.geom.outwards, self.dyn.inwards, {"weight": "weight_rocket"})

        self.add_inward_modevar(
            "flying", False, desc="Whether the rocket is flying or not", unit=""
        )

        self.add_event("Takeoff", trigger="stage_1.engine.force > 0")

    def compute(self):
        self.a *= self.flying

    def transition(self):

        if self.Takeoff.present:
            self.flying = True
