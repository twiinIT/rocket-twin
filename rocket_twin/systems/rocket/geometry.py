import numpy as np
from cosapp.base import System
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import TopoDS_Solid

# from OCC.Display.SimpleGui import init_display


class Geometry(System):
    """Geometrical properties of a system.

    Inputs
    ------
    shapes: TopoDS_Solid,
        pyoccad models of each component of the system
    densities [kg/m**3]: float,
        densities of each component of the system

    Outputs
    ------
    cg [m]: float,
        center of gravity
    weight [kg]: float,
        total weight
    I [kg*m**2] : float,
        Inertia matrix
    """

    def setup(self, shapes=None, densities=None):

        if shapes is None:
            shapes = []
        if densities is None:
            densities = []

        self.add_property("shapes", shapes)
        self.add_property("densities", densities)

        for shape in shapes:
            self.add_inward(shape, TopoDS_Solid(), desc=f"shape of {shape}")
        for density in densities:
            self.add_inward(density, 1.0, desc=f"Density of {density}", unit="kg/m**3")

        self.add_outward("weight", 1.0, desc="weight", unit="kg")
        self.add_outward("cg", 1.0, desc="center of gravity", unit="m")
        self.add_outward("I", np.empty((3, 3)), desc="Inertia matrix", unit="kg*m**2")

    def compute(self):

        vprop = GProp_GProps()
        for i in range(len(self.shapes)):
            vprop_int = GProp_GProps()
            brepgprop.VolumeProperties(self[self.shapes[i]], vprop_int)
            vprop.Add(vprop_int, self[self.densities[i]])

        self.weight = vprop.Mass()
        self.cg = vprop.CentreOfMass().Z()

        inertia = vprop.MatrixOfInertia()
        for i, j in zip(range(3), range(3)):
            self.I[i, j] = inertia.Value(i + 1, j + 1)

    # def view(self):

    # display, start_display, add_menu, add_function_to_menu = init_display()

    # for shape in self.shapes:
    # display.DisplayColoredShape(self[shape], "RED")

    # start_display()
