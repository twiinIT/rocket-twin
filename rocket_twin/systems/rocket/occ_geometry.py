import numpy as np
from cosapp.base import System
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Solid
from pyoccad.create import CreateSphere

# from OCC.Display.SimpleGui import init_display


class OCCGeometry(System):
    """Geometrical properties of a system.

    Inputs
    ------
    shapes: TopoDS_Solid, TopoDS_Compound,
        pyoccad models of each component of the system
    props: GProp_GProps,
        properties of each model

    Outputs
    ------
    shapes: TopoDS_Solid, TopoDS_Compound,
        fusion of all input models
    props: GProp_GProps,
        properties of the global model
    cg [m]: float,
        center of gravity
    weight [kg]: float,
        total weight
    I [kg*m**2] : float,
        Inertia matrix
    """

    def setup(self, shapes=None, properties=None):

        if shapes is None:
            shapes = []
        if properties is None:
            properties = []

        self.add_property("shapes", shapes)
        self.add_property("properties", properties)

        for shape in shapes:
            self.add_inward(
                shape,
                TopoDS_Solid(),
                dtype=(TopoDS_Solid, TopoDS_Compound),
                desc=f"shape of {shape}",
            )
        for props in properties:
            self.add_inward(props, GProp_GProps(), desc=f"Properties of the {props}")

        self.add_outward(
            "shape",
            CreateSphere.from_radius_and_center(1.0),
            dtype=(TopoDS_Solid, TopoDS_Compound),
            desc="global shape",
        )
        self.add_outward("props", GProp_GProps(), desc="global properties")
        self.add_outward("weight", 1.0, desc="weight", unit="kg")
        self.add_outward("cg", 1.0, desc="center of gravity", unit="m")
        self.add_outward("I", np.empty((3, 3)), desc="Inertia matrix", unit="kg*m**2")

    def compute(self):

        self.props = GProp_GProps()
        for props in self.properties:
            self.props.Add(self[props])

        try:
            self.shape = self.fusion(self.shapes)
        except TypeError:
            pass

        self.weight = self.props.Mass()
        self.cg = self.props.CentreOfMass().Z()

        inertia = self.props.MatrixOfInertia()
        for i, j in zip(range(3), range(3)):
            self.I[i, j] = inertia.Value(i + 1, j + 1)

    def fusion(self, shapes):

        shape_list = shapes.copy()
        fusion = self[shape_list.pop(0)]
        for shape in shape_list:
            fusion = BRepAlgoAPI_Fuse(fusion, self[shape]).Shape()

        return fusion

    # def view(self):

    # display, start_display, add_menu, add_function_to_menu = init_display()

    # for shape in self.shapes:
    # display.DisplayColoredShape(self[shape], "RED")

    # start_display()
