import numpy as np
from cosapp.base import System
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCylinder, CreateSphere


class TubeGeom(System):
    """Pyoccad model of a solid tube.

    Inputs
    ------

    Outputs
    ------
    shape: TopoDS_Solid,
        pyoccad model
    props: GProp_GProps,
        model properties
    """

    def setup(self):

        # Geometric parameters
        self.add_inward("radius", 1.0, desc="internal radius", unit="m")
        self.add_inward("length", 5.0, desc="length", unit="m")

        # Density
        self.add_inward("rho", 0.2 / np.pi, desc="density", unit="kg/m**3")

        # Positional parameters
        self.add_inward("pos", 1.0, desc="lowest point z coordinate", unit="m")

        # Outputs
        self.add_outward("shape", CreateSphere.from_radius_and_center(1.0), desc="pyoccad model")
        self.add_outward("props", GProp_GProps(), desc="model properties")

    def compute(self):

        self.shape = CreateCylinder().from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(0, 0, self.length), self.radius
        )
        vprop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, vprop)
        self.props = GProp_GProps()
        self.props.Add(vprop, self.rho)
