from cosapp.base import System

from rocket_twin.systems import Dynamics, Engine, Tank


class Rocket(System):
    """A simple model of a rocket.

    Inputs
    ------

    Outputs
    ------
    """

    def setup(self):
        self.add_child(Engine("engine"))
        self.add_child(Tank("tank"), pulling=["w_in"])
        self.add_child(
            Dynamics(
                "dyn",
                forces=["thrust"],
                weights=["weight_eng", "weight_tank"],
                centers=["engine", "tank"],
            ),
            pulling=["a"],
        )

        self.connect(
            self.engine.outwards,
            self.dyn.inwards,
            {"force": "thrust", "weight": "weight_eng", "cg": "engine"},
        )
        self.connect(self.tank.outwards, self.dyn.inwards, {"weight": "weight_tank", "cg": "tank"})

        # Event
        self.add_event("is_flying", trigger="a > 0")

    def transition(self):
        if self.is_flying.present:
            self.dyn.flight = True
