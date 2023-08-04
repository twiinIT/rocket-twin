import numpy as np
from cosapp.base import System
from OCC.Core.gp import gp_Pnt, gp_Vec
from pyoccad.create import CreateCylinder


class Tube(System):
    """A simple model of a tube.

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
        self.add_inward("radius", 1.0, desc="internal radius", unit="m")
        self.add_inward("length", 5.0, desc="length", unit="m")

        # Positional parameters
        self.add_inward("pos", 1.0, desc="lowest point z coordinate", unit="m")

        # Pyoccad model
        shape = CreateCylinder().from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(0, 0, self.length), self.radius
        )

        # Outputs
        self.add_outward("shape", shape, desc="pyoccad model")
        self.add_outward("rho", 0.2 / np.pi, desc="density", unit="kg/m**3")
