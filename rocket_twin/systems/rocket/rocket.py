from cosapp.base import System

from rocket_twin.systems import ControllerCoSApp, Dynamics, Engine, Nose, Tank, Tube, Wings
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
        self.add_child(Tank("tank"), pulling=["w_in", "weight_max", "weight_p"])
        self.add_child(Engine("engine"))
        self.add_child(Nose("nose"))
        self.add_child(Tube("tube"))
        self.add_child(Wings("wings"))
        self.add_child(
            OCCGeometry(
                "geom",
                shapes=["tank", "engine", "nose", "tube", "wings"],
                densities=["rho_tank", "rho_engine", "rho_nose", "rho_tube", "rho_wings"],
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

        self.connect(self.tank.outwards, self.geom.inwards, {"shape": "tank", "rho": "rho_tank"})
        self.connect(
            self.engine.outwards, self.geom.inwards, {"shape": "engine", "rho": "rho_engine"}
        )
        self.connect(self.nose.outwards, self.geom.inwards, {"shape": "nose", "rho": "rho_nose"})
        self.connect(self.tube.outwards, self.geom.inwards, {"shape": "tube", "rho": "rho_tube"})
        self.connect(self.wings.outwards, self.geom.inwards, {"shape": "wings", "rho": "rho_wings"})

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
