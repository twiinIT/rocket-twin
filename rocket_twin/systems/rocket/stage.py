from cosapp.base import System

from rocket_twin.systems import ControllerCoSApp, Engine, NoseGeom, Tank, TubeGeom, WingsGeom
from rocket_twin.systems.rocket import OCCGeometry


class Stage(System):
    """Model of a rocket stage.

    Inputs
    ------

    Outputs
    ------
    force [N]: float,
        thrust force
    weight [kg]: float,
        weight
    cg [m]: float,
        center of gravity
    """

    def setup(self, nose=False, wings=False):

        shapes = ["tank_s", "engine_s", "tube_s"]
        properties = ["tank", "engine", "tube"]

        self.add_child(ControllerCoSApp("controller"), pulling=['is_on'])
        self.add_child(Tank("tank"), pulling=["w_in", "weight_max", "weight_prop"])
        self.add_child(Engine("engine"), pulling={"force": "thrust"})
        self.add_child(TubeGeom("tube"))

        if nose:
            self.add_child(NoseGeom("nose"))
            shapes.append("nose_s")
            properties.append("nose")

        if wings:
            self.add_child(WingsGeom("wings"))
            shapes.append("wings_s")
            properties.append("wings")

        self.add_child(
            OCCGeometry("geom", shapes=shapes, properties=properties), pulling=["shape", "props"]
        )

        self.connect(self.controller.outwards, self.tank.inwards, {"w": "w_command"})
        self.connect(self.tank.outwards, self.engine.inwards, {"w_out": "w_out"})

        for prop in properties:
            self.connect(
                self[prop].outwards, self.geom.inwards, {"shape": prop + "_s", "props": prop}
            )
