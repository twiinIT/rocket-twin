import numpy as np
from cosapp.base import System
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_XYZ
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCylinder


class TankGeom(System):
    """Tank geometry.

    Inputs
    ------

    Outputs
    ------
    rho [kg/m**3]: float,
        mean density
    shape: TopoDS_Solid
        pyoccad model
    """

    def setup(self):

        # Geometry
        self.add_inward("radius", 1.0, desc="Base radius", unit="m")
        self.add_inward("height", 1 / np.pi, desc="Height", unit="m")

        # Weight
        self.add_inward("weight", 1.0, desc="current weight", unit="kg")

        # Position
        self.add_inward("pos", 1 - 1 / np.pi, desc="base center z-coordinate", unit="m")

        # Outputs
        init = CreateCylinder.from_base_and_dir(gp_Pnt(0, 0, 0), gp_Vec(gp_XYZ(0, 0, 1)), 0)
        self.add_outward("shape", init, desc="pyoccad model")
        self.add_outward("rho", 0.0, desc="Mean density", unit="kg/m**3")

    def compute(self):

        self.shape = CreateCylinder.from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(gp_XYZ(0, 0, self.height)), self.radius
        )

        v_prop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, v_prop)
        self.rho = self.weight / v_prop.Mass()
