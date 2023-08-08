import numpy as np
from cosapp.base import System
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCylinder


class TankFuel(System):
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
        pyoccad model
    """

    def setup(self):

        # Fuel
        self.add_inward("weight_max", 5.0, desc="Maximum fuel capacity", unit="kg")
        self.add_inward("rho", 1., desc="Fuel density", unit="kg/m**3")

        # Geometry
        self.add_inward("r_int", 1., desc="internal radius", unit='m')

        # Flux control
        self.add_inward("w_out_max", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_inward("w_command", 1.0, desc="Fuel output control variable", unit="")

        # Inputs
        self.add_inward("w_in", 0.0, desc="Fuel income rate", unit="kg/s")

        # Outputs
        init = CreateCylinder.from_base_and_dir(gp_Pnt(0, 0, 0), gp_Vec(gp_Pnt(0, 0, 1)), 0)
        self.add_outward("w_out", 0.0, desc="Fuel output rate", unit="kg/s")
        self.add_outward("shape", init, desc="Fuel pyoccad model")
        self.add_outward("props", GProp_GProps(), desc="model properties")

        # Transient
        self.add_transient("weight_p", der="w_in - w_out", desc="Propellant weight")

    def compute(self):

        self.w_out = self.w_out_max * self.w_command

        height = self.weight_p / (np.pi * self.r_int**2 * self.rho) + 0.0001
        radius = self.r_int
        self.shape = CreateCylinder.from_base_and_dir(gp_Pnt(0, 0, self.pos), gp_Vec(gp_Pnt(0, 0, height)), radius)

        vprop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, vprop)
        self.props = GProp_GProps()
        self.props.Add(vprop, self.rho)
        

    
