import numpy as np
from cosapp.base import System
from OCC.Core.GProp import GProp_GProps
from math import pi

from rocket_twin.systems import Dynamics, RocketControllerCoSApp
from rocket_twin.systems.rocket import OCCGeometry, Stage


class Rocket(System):
    """A simple model of a rocket.

    Inputs
    ------
    flying: boolean,
        whether the rocket is already flying or still on ground
    n_stages: int,
        how many stages the rocket has

    Values
    ------
    shapes: list[TopoDS_Shape],
        pyoccad visual representation of each component
    properties: list[GProp_Gprops],
        volume properties of each component's pyoccad model
    forces [N]: list [float],
        total force in each stage

    Outputs
    ------
    a [m/s**2]: float,
        rocket acceleration
    """

    def setup(self, n_stages=1):

        shapes, properties, forces = ([None] * n_stages for i in range(3))

        #parameter for rotating the rocket
        self.add_inward("teta", 2*pi/180, desc="rocket rotation angle")
        self.add_inward("Hm", 6500.0e3 , desc ="maneuvering altitude at which we want the rocket to rotate")
        self.add_inward("rotate", True , desc ="condition for rotating")

        self.add_inward("n_stages", n_stages, desc="Number of stages")
        self.add_outward("stage", 1, desc="Current stage")
        self.add_inward("flying", False, desc="Whether the rocket is flying or not")

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
                    "weight_prop": f"weight_prop_{i}", "v":"v"
                },
            )
            shapes[i - 1] = f"stage_{i}_s"
            properties[i - 1] = f"stage_{i}"
            forces[i - 1] = f"thrust_{i}"

        self.add_child(
            RocketControllerCoSApp("controller", n_stages=n_stages),
            execution_index=0,
            pulling=["flying"],
        )
        self.add_child(OCCGeometry("geom", shapes=shapes, properties=properties))
        self.add_child(
            Dynamics("dyn", forces=forces, weights=["weight_rocket"]), pulling=["a", "pos"]
        )  # pulling acceleration and position to dynamics

        for i in range(1, n_stages + 1):
            self.connect(
                self.controller.outwards, self[f"stage_{i}"].inwards, {f"is_on_{i}": "is_on"}
            )
            self.connect(
                self[f"stage_{i}"].outwards,
                self.controller.inwards,
                {"weight_prop": f"weight_prop_{i}"},
            )
            self.connect(self[f"stage_{i}"].outwards, self.geom.inwards, {"props": f"stage_{i}"})
            self.connect(self[f"stage_{i}"].outwards, self.dyn.inwards, {"thrust": f"thrust_{i}"})

        self.connect(self.geom.outwards, self.dyn.inwards, {"weight": "weight_rocket"})

        self.add_event("rotation", trigger = "pos[2] >= Hm")  # if we reach the altitude Hm, we want to rotate the rocket

    def compute(self):
        self.a *= self.flying #if the whole rocket is not flying, its acceleration is False = 0

    def transition(self):  
        
        if self.rotation.present:  # rotate the speed vector around y-axis by multiplying by rotation matrix at a given height (Hm)
            self.v = np.dot(np.array([[np.cos(self.teta), 0, np.sin(self.teta)], [0, 1, 0], [-np.sin(self.teta), 0, np.cos(self.teta)]]),self.v.T ) 

        if self.controller.drop.present: #change active stage when it runs out of propellant (mass = 0)
            if self.stage < self.n_stages:
                stage = self.pop_child(f"stage_{self.stage}")
                self.add_child(stage, execution_index=self.stage - 1)
                self.geom[f"stage_{self.stage}"] = GProp_GProps()
                self.dyn[f"thrust_{self.stage}"] = np.zeros(3)
                self.stage += 1
