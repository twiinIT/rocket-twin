from cosapp.base import System

from rocket_twin.systems.tank import TankFuel, TankGeom


class Tank(System):
    """A simple model of a fuel tank.

    Inputs
    ------
    w_in [kg/s]: float,
        mass flow of fuel entering the tank
    w_command: float,
        fuel exit flux control. 0 means tank exit fully closed, 1 means fully open

    Outputs
    ------
    w_out [kg/s]: float,
        mass flow of fuel exiting the tank
    shape: TopoDS_Solid,
        pyoccad model of the structure and fuel
    props: GProp_GProps,
        model properties
    """

    def setup(self):

        self.add_child(
            TankFuel("fuel"), pulling=["w_out", "w_in", "w_command", "weight_max", "weight_p"]
        )
        self.add_child(TankGeom("geom"), pulling=["shape", "props"])

        self.connect(self.geom.inwards, self.fuel.inwards, ["weight_p"])
