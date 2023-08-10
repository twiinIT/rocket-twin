import numpy as np
from cosapp.base import System
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCircle, CreateCylinder, CreateExtrusion, CreateFace


class TankGeom(System):
    """Pyoccad model of the tank structure and fuel.

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

        # Structure parameters
        self.add_inward("r_int", 0.8, desc="internal radius", unit="m")
        self.add_inward("r_ext", 1.0, desc="external radius", unit="m")
        self.add_inward("thickness", self.r_ext - self.r_int, desc="thickness", unit="m")
        self.add_inward("height", 1.0, desc="Height", unit="m")
        self.add_inward("rho_struct", 1 / (0.56 * np.pi), desc="Structure density", unit="kg/m**3")

        # Fuel parameters
        self.add_inward("weight_prop", 0.0, desc="Fuel weight", unit="kg")
        self.add_inward("rho_fuel", 7.8125 / np.pi, desc="Fuel density", unit="kg/m**3")

        # Position
        self.add_inward("pos", 0.0, desc="base center z-coordinate", unit="m")

        # Outputs
        self.add_outward("shape", CreateCylinder(), desc="pyoccad model")
        self.add_outward("props", GProp_GProps(), desc="model properties")
        self.add_outward("weight_max", 1.0, desc="Maximum fuel capacity", unit="kg")

    def compute(self):

        self.weight_max = np.pi * self.r_int**2 * self.height * self.rho_fuel

        height_fuel = self.weight_prop / (np.pi * self.r_int**2 * self.rho_fuel) + 0.00000001

        shape_struct = self.create_structure(
            self.r_int, self.r_ext, self.height, self.thickness, self.pos
        )
        shape_fuel = CreateCylinder.from_base_and_dir(
            gp_Pnt(0, 0, self.pos), gp_Vec(0, 0, height_fuel), self.r_int
        )
        self.shape = BRepAlgoAPI_Fuse(shape_struct, shape_fuel).Shape()

        fuel_prop = GProp_GProps()
        struct_prop = GProp_GProps()
        brepgprop.VolumeProperties(shape_struct, struct_prop)
        brepgprop.VolumeProperties(shape_fuel, fuel_prop)

        self.props = GProp_GProps()
        self.props.Add(fuel_prop, self.rho_fuel)
        self.props.Add(struct_prop, self.rho_struct)

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
