import numpy as np
from cosapp.base import System
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import TopoDS_Solid
from pyoccad.create import CreateCone


class Engine(System):
    """Simple model of an engine.

    Inputs
    ------
    w_out [kg/s]: float,
        fuel consumption rate

    Outputs
    ------
    force [N]: float,
        thrust force
    shape: TopoDS_Solid,
        pyoccad model
    props: GProp_GProps,
        model properties
    """

    def setup(self):

        # Inputs
        self.add_inward("w_out", 0.0, desc="Fuel consumption rate", unit="kg/s")

        # Parameters
        self.add_inward("isp", 20.0, desc="Specific impulsion in vacuum", unit="s")
        self.add_inward("g_0", 10.0, desc="Gravity at Earth's surface", unit="m/s**2")

        # Geometric parameters
        self.add_inward("base_radius", 1.0, desc="Base radius", unit="m")
        self.add_inward("top_radius", 0.5, desc="top radius", unit="m")
        self.add_inward("height", 1.0, desc="Height", unit="m")

        # Density
        self.add_inward("rho", 12 / (7 * np.pi), desc="density", unit="kg/m**3")

        # Positional parameters
        self.add_inward("pos", -1 / np.pi, desc="Base center z-position", unit="m")

        # Outputs
        self.add_outward("shape", TopoDS_Solid(), desc="pyoccad model")
        self.add_outward("props", GProp_GProps(), desc="model properties")
        self.add_outward("force", 1.0, desc="Thrust force", unit="N")

    def compute(self):

        self.force = self.isp * self.w_out * self.g_0
        self.shape = CreateCone.from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(0, 0, self.height), self.base_radius, self.top_radius
        )
        vprop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, vprop)
        self.props = GProp_GProps()
        self.props.Add(vprop, self.rho)
