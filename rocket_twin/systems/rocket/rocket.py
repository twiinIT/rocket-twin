from cosapp.base import System

from rocket_twin.systems import ControllerCoSApp, Dynamics, Engine, Tank


class Rocket(System):
    """A simple model of a rocket.

    Inputs
    ------
    flying: boolean,
        whether the rocket is already flying or still on ground

    Outputs
    ------
    """

    def setup(self):
        self.add_child(ControllerCoSApp("controller"))
        self.add_child(Tank("tank"), pulling=["w_in", "weight_max", "weight_p"])
        self.add_child(Engine("engine"))
        self.add_child(
            Dynamics(
                "dyn",
                forces=["thrust"],
                weights=["weight_eng", "weight_tank"],
                centers=["engine", "tank"],
            ),
            pulling=["a"],
        )

        self.connect(self.controller.outwards, self.tank.inwards, {"w": "w_command"})
        self.connect(self.tank.outwards, self.engine.inwards, {"w_out": "w_out"})

        self.connect(
            self.engine.outwards,
            self.dyn.inwards,
            {"force": "thrust", "weight": "weight_eng", "cg": "engine"},
        )
        self.connect(self.tank.outwards, self.dyn.inwards, {"weight": "weight_tank", "cg": "tank"})

        self.add_inward_modevar(
            "flying", False, desc="Whether the rocket is flying or not", unit=""
        )

        self.add_event("Takeoff", trigger="engine.force > 0")

    def compute(self):
        self.a *= self.flying

    def transition(self):

        if self.Takeoff.present:
            self.flying = True
