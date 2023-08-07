import numpy as np
from cosapp.base import System
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.TopoDS import TopoDS_Solid
from pyoccad.create import CreateCone


class Nose(System):
    """A simple model of a nose.

    Inputs
    ------

    Outputs
    ------
    rho [kg/m**3]: float,
        density
    shape: TopoDS_Solid,
        pyoccad model
    """

    def setup(self):

        # Geometric parameters
        self.add_inward("radius", 1.0, desc="Base radius", unit="m")
        self.add_inward("height", 1.0, desc="Height", unit="m")

        # Positional parameters
        self.add_inward("pos", 6.0, desc="Base center z-position", unit="m")

        # Outputs
        self.add_outward("shape", TopoDS_Solid(), desc="pyoccad model")
        self.add_outward("rho", 3 / np.pi, desc="density", unit="kg/m**3")

    def compute(self):

        self.shape = CreateCone.from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(0, 0, self.height), self.radius
        )
