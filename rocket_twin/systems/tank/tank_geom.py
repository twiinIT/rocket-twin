import numpy as np
from cosapp.base import System
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCylinder, CreateCircle, CreateExtrusion, CreateFace


class TankGeom(System):
    """Pyoccad model of the tank structure.

    Inputs
    ------

    Outputs
    ------
    shape: TopoDS_Solid,
        pyoccad model
    """

    def setup(self):

        # Geometry
        self.add_inward("r_int", 1.0, desc="internal radius", unit="m")
        self.add_inward("r_ext", 2.0, desc="external radius", unit='m')
        self.add_inward("thickness", self.r_ext - self.r_int, desc="thickness", unit='m')
        self.add_inward("height", 1 / np.pi, desc="Height", unit="m")

        # Density
        self.add_inward("rho", 0.0, desc="Structure density", unit="kg/m**3")

        # Position
        self.add_inward("pos", 1 - 1 / np.pi, desc="base center z-coordinate", unit="m")

        # Outputs
        init = CreateCylinder.from_base_and_dir(gp_Pnt(0, 0, 0), gp_Vec(gp_Pnt(0, 0, 1)), 0)
        self.add_outward("shape", init, desc="pyoccad structure model")
        self.add_outward("props", GProp_GProps(), desc="model properties")

    def compute(self):

        self.shape = self.create_structure(self.r_int, self.r_ext, self.height, self.thickness, self.pos)
        vprop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, vprop)
        self.props = GProp_GProps()
        self.props.Add(vprop, self.rho)

    def create_structure(self, r_int, r_ext, height, thickness, pos):
        """Create a pyoccad model of an empty cylindrical tank.

        Inputs
        ------
        r_int: float,
            internal radius
        r_ext: float,
            external radius
        pos: float,
            base center z-coordinate
        height: float,
            height
        thickness: float,
            base thickness

        Outputs
        ------
        tank: TopoDS_Solid,
            pyoccad model of the set of wings
        """

        center = gp_Pnt(0, 0, pos)
        vector_up = gp_Vec(0, 0, height)
        vector_down = gp_Vec(0, 0, -thickness)

        cont_int = CreateCircle.from_radius_and_center(r_int, center)
        cont_ext = CreateCircle.from_radius_and_center(r_ext, center)

        circ_int = CreateFace.from_contour(cont_int)
        circ_ext = CreateFace.from_contour(cont_ext)

        cyl_int = CreateExtrusion.surface(circ_int, vector_up)
        cyl_ext = CreateExtrusion.surface(circ_ext, vector_up)
        bottom = CreateExtrusion.surface(circ_ext, vector_down)

        shell = BRepAlgoAPI_Cut(cyl_ext, cyl_int).Shape()
        tank = BRepAlgoAPI_Fuse(shell, bottom).Shape()

        return tank
        
