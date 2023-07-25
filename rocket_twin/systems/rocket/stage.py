from cosapp.base import System

from rocket_twin.systems import ControllerCoSApp, Engine, Tank


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

    def setup(self):

        self.add_child(ControllerCoSApp("controller"))
        self.add_child(Tank("tank"), pulling=["w_in", "weight_max", "weight_p"])
        self.add_child(Engine("engine"), pulling=["force"])

        self.connect(self.controller.outwards, self.tank.inwards, {"w": "w_command"})
        self.connect(self.tank.outwards, self.engine.inwards, {"w_out": "w_out"})

        self.add_outward("weight", 1.0, desc="Weight", unit="kg")
        self.add_outward("cg", 1.0, desc="Center of gravity", unit="m")

        self.tank.w_out_max = 1.
        self.weight_p = self.weight_max

    def compute(self):

        print("COMPUTANDO")
        self.weight = self.tank.weight + self.engine.weight
        self.cg = (self.tank.cg * self.tank.weight + self.engine.cg * self.engine.weight) / (
            self.weight
        )
