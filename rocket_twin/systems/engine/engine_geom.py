import numpy as np
from cosapp.base import System
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCone


class EngineGeom(System):
    """Pyoccad model of an engine.

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
        self.add_inward("base_radius", 1.0, desc="Base radius", unit="m")
        self.add_inward("top_radius", 0.5, desc="top radius", unit="m")
        self.add_inward("height", 1.0, desc="Height", unit="m")

        # Density
        self.add_inward("rho", 12 / (7 * np.pi), desc="density", unit="kg/m**3")

        # Positional parameters
        self.add_inward("pos", -1.2, desc="Base center z-position", unit="m")

        # Outputs
        self.add_outward("shape", CreateCone(), desc="pyoccad model")
        self.add_outward("props", GProp_GProps(), desc="model properties")

    def compute(self):

        self.shape = CreateCone.from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(0, 0, self.height), self.base_radius, self.top_radius
        )
        vprop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, vprop)
        self.props = GProp_GProps()
        self.props.Add(vprop, self.rho)
