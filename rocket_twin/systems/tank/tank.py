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
    weight_prop [kg]: float,
        fuel weight
    weight_max [kg]: float,
        maximum fuel capacity
    shape: TopoDS_Solid,
        pyoccad model of the structure and fuel
    props: GProp_GProps,
        model properties
    """

    def setup(self):

        self.add_child(TankFuel("fuel"), pulling=["w_out", "w_in", "w_command", "weight_prop"])
        self.add_child(TankGeom("geom"), pulling=["shape", "props", "weight_max"])

        self.connect(self.fuel.outwards, self.geom.inwards, ["weight_prop"])
