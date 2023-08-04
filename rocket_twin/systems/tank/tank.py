import numpy as np
from cosapp.base import System
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_XYZ
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCylinder


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
    weight [kg]: float,
        weight
    cg [m]: float,
        center of gravity
    """

    def setup(self):

        # Geometry
        self.add_inward("radius", 1.0, desc="Base radius", unit="m")
        self.add_inward("height", 1 / np.pi, desc="Height", unit="m")

        # Fuel
        self.add_inward("weight_s", 1.0, desc="Structure weight", unit="kg")
        self.add_inward("weight_max", 5.0, desc="Maximum fuel capacity", unit="kg")

        # Position
        self.add_inward('pos', 1 - 1/np.pi, desc="base center z-coordinate", unit='m')

        # pyoccad model
        shape = CreateCylinder.from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(gp_XYZ(0, 0, self.height)), self.radius
        )

        # Inputs
        self.add_inward("w_in", 0.0, desc="Fuel income rate", unit="kg/s")

        # Flux control
        self.add_inward("w_out_max", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_inward("w_command", 1.0, desc="Fuel output control variable", unit="")

        # Outputs
        self.add_outward("w_out", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_outward("shape", shape, desc="pyoccad model")
        self.add_outward("rho", 0.0, desc="Mean density", unit="kg/m**3")

        # Transient
        self.add_transient("weight_p", der="w_in - w_out", desc="Propellant weight")

    def compute(self):
        self.w_out = self.w_out_max * self.w_command

        weight = self.weight_s + self.weight_p
        v_prop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, v_prop)
        self.rho = weight / v_prop.Mass()
