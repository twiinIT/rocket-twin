from cosapp.base import System

from rocket_twin.systems import (
    ControllerCoSApp,
    Dynamics,
    Engine,
    NoseGeom,
    Tank,
    TubeGeom,
    WingsGeom,
)
from rocket_twin.systems.rocket import OCCGeometry


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
        self.add_child(Tank("tank"), pulling=["w_in", "weight_max", "weight_prop"])
        self.add_child(Engine("engine"))
        self.add_child(NoseGeom("nose"))
        self.add_child(TubeGeom("tube"))
        self.add_child(WingsGeom("wings"))
        self.add_child(
            OCCGeometry(
                "geom",
                shapes=["tank_s", "engine_s", "nose_s", "tube_s", "wings_s"],
                properties=["tank", "engine", "nose", "tube", "wings"],
            )
        )
        self.add_child(
            Dynamics(
                "dyn",
                forces=["thrust"],
                weights=["weight_rocket"],
            ),
            pulling=["a"],
        )

        self.connect(self.controller.outwards, self.tank.inwards, {"w": "w_command"})
        self.connect(self.tank.outwards, self.engine.inwards, {"w_out": "w_out"})

        self.connect(self.tank.outwards, self.geom.inwards, {"shape": "tank_s", "props": "tank"})
        self.connect(
            self.engine.outwards, self.geom.inwards, {"shape": "engine_s", "props": "engine"}
        )
        self.connect(self.nose.outwards, self.geom.inwards, {"shape": "nose_s", "props": "nose"})
        self.connect(self.tube.outwards, self.geom.inwards, {"shape": "tube_s", "props": "tube"})
        self.connect(self.wings.outwards, self.geom.inwards, {"shape": "wings_s", "props": "wings"})

        self.connect(
            self.engine.outwards,
            self.dyn.inwards,
            {"force": "thrust"},
        )

        self.connect(self.geom.outwards, self.dyn.inwards, {"weight": "weight_rocket"})

        self.add_inward_modevar(
            "flying", False, desc="Whether the rocket is flying or not", unit=""
        )

        self.add_event("Takeoff", trigger="engine.force > 0")
        # self.add_event("view", trigger="t == 0.2")

    def compute(self):
        self.a *= self.flying

    def transition(self):

        if self.Takeoff.present:
            self.flying = True
        # if self.view.present:
        # self.geom.view()
