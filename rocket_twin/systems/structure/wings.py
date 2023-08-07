import numpy as np
from cosapp.base import System
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.TopoDS import TopoDS_Solid
from pyoccad.create import CreateEdge, CreateExtrusion, CreateFace, CreateTopology, CreateWire


class Wings(System):
    """A simple model of a set of wings.

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
        self.add_inward("n", 4, desc="Number of wings", unit="")
        self.add_inward("l_in", 1.0, desc="rocket edge length", unit="m")
        self.add_inward("l_out", 0.5, desc="free edge length", unit="m")
        self.add_inward("width", 4 / 3, desc="width", unit="m")
        self.add_inward("th", 0.1, desc="thickness", unit="m")

        # Positional parameters
        self.add_inward("radius", 1.0, desc="radius of the set", unit="m")
        self.add_inward("pos", 0.75, desc="lowest point z-coordinate", unit="m")

        # Outputs
        self.add_outward("shape", TopoDS_Solid(), desc="pyoccad model")
        self.add_outward("rho", 10.0, desc="density", unit="kg/m**3")

    def compute(self):

        self.shape = self.create_wings(
            self.n, self.radius, self.pos, self.l_in, self.l_out, self.width, self.th
        )

    def create_wings(self, n_wings, radius, pos, l_in, l_out, width, th):
        """Create a pyoccad model of a set of wings.

        Inputs
        ------
        n_wings: int,
            the number of wings
        radius: float,
            the distance of the internal edges to the center
        pos: float,
            the lower edges' z-coordinate
        l_in: float,
            the length of the inner edges
        l_out: float,
            the length of the outer edges
        width: float,
            width
        th: float,
            thickness

        Outputs
        ------

        fusion: TopoDS_Solid,
            pyoccad model of the set of wings
        """

        theta = 2 * np.pi / n_wings
        shapes = [None] * n_wings

        for i in range(n_wings):

            ang = theta * i

            p1 = gp_Pnt(radius * np.cos(ang), radius * np.sin(ang), pos)
            p2 = gp_Pnt((radius + width) * np.cos(ang), (radius + width) * np.sin(ang), pos)
            p3 = gp_Pnt((radius + width) * np.cos(ang), (radius + width) * np.sin(ang), pos + l_out)
            p4 = gp_Pnt(radius * np.cos(ang), radius * np.sin(ang), pos + l_in)

            edge1 = CreateEdge().from_2_points(p1, p2)
            edge2 = CreateEdge().from_2_points(p2, p3)
            edge3 = CreateEdge().from_2_points(p3, p4)
            edge4 = CreateEdge().from_2_points(p4, p1)

            contour = CreateWire().from_elements([edge1, edge2, edge3, edge4])
            face = CreateFace().from_contour(contour)
            shell = CreateExtrusion().surface(face, gp_Vec(-th * np.sin(ang), th * np.cos(ang), 0))
            shapes[i] = CreateTopology().make_solid(shell)

        fusion = BRepAlgoAPI_Fuse(shapes[0], shapes[1]).Shape()

        for i in range(2, n_wings):
            fusion = BRepAlgoAPI_Fuse(fusion, shapes[i]).Shape()

        return fusion
