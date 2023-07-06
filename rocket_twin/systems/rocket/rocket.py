from cosapp.base import System

from rocket_twin.systems import Dynamics, Engine, Tank, Nose, Tube, Wings


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
        self.add_child(Nose('nose'))
        self.add_child(Tube('tube'))
        self.add_child(Wings('wings'))
        self.add_child(Engine("engine"), pulling=["force_command"])
        self.add_child(Tank("tank"), pulling=["w_in", "w_command"])
        self.add_child(
            Dynamics(
                "dyn",
                forces=["thrust"],
                weights=["weight_eng", "weight_tank", "weight_nose", "weight_tube", "weight_wings"],
                centers=["engine", "tank", "nose", "tube", "engine"],
            ),
            pulling=["a"],
        )

        self.connect(self.tank.outwards, self.engine.inwards, ['w_out'])
        self.connect(
            self.engine.outwards,
            self.dyn.inwards,
            {"force": "thrust", "weight": "weight_eng", "cg": "engine"},
        )
        self.connect(self.tank.outwards, self.dyn.inwards, {"weight": "weight_tank", "cg": "tank"})
        self.connect(self.nose.outwards, self.dyn.inwards, {'weight' : 'weight_nose', 'cg' : 'nose'})
        self.connect(self.tube.outwards, self.dyn.inwards, {'weight' : 'weight_tube', 'cg' : 'tube'})
        self.connect(self.wings.outwards, self.dyn.inwards, {'weight' : 'weight_wings', 'cg' : 'wings'})

        self.add_inward("flying", False, desc="Whether the rocket is flying or not", unit="")

    def compute(self):
        self.a *= self.flying
