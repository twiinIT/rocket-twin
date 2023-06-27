from cosapp.base import System

from rocket_twin.systems import Dynamics, Engine, Tank
from rocket_twin.systems.rocket import RocketGeom


class Rocket(System):
    def setup(self):
        self.add_child(Engine("engine"))
        self.add_child(Tank("tank"), pulling=["p_in"])
        self.add_child(
            RocketGeom("geom", centers=["engine", "tank"], weights=["weight_eng", "weight_tank"])
        )
        self.add_child(
            Dynamics("dyn", forces=["thrust"], weights=["weight_eng", "weight_tank"])
        )

        self.connect(
            self.engine.outwards, self.geom.inwards, {"cg": "engine", "weight": "weight_eng"}
        )
        self.connect(self.tank.outwards, self.geom.inwards, {"cg": "tank", "weight": "weight_tank"})
        self.connect(
            self.engine.outwards, self.dyn.inwards, {"force": "thrust", "weight": "weight_eng"}
        )
        self.connect(self.tank.outwards, self.dyn.inwards, {"weight": "weight_tank"})

        self.exec_order = ["engine", "tank", "geom", "dyn"]
