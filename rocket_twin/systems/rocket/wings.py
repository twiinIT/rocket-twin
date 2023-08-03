from cosapp.base import System
from pyoccad.create import CreateExtrusion, CreateEdge, CreateWire, CreateTopology, CreateFace
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
import numpy as np

class Wings(System):

    def setup(self):

        # Geometric parameters
        self.add_inward('l_in', 2., desc="rocket edge length", unit='m')
        self.add_inward('l_out', 1., desc="free edge length", unit='m')
        self.add_inward('height', 1., desc="height", unit='m')
        self.add_inward('th', 0.1, desc="thickness", unit='m')

        # Pyoccad model
        shape = self.create_wing(self.l_in, self.l_out, self.height, self.th)
        self.add_inward('shape', shape, desc="pyoccad model")

        # Outputs
        self.add_outward('weight', 1., desc="weight", unit='kg')
        self.add_outward('cg', 1., desc="center of gravity", unit='m')
        self.add_outward('I', np.empty((3,3)), desc="Inertia tensor", unit='kg*m**2')

    def compute(self):

        vprop = GProp_GProps()
        brepgprop.VolumeProperties(self.shape, vprop)
        inertia = vprop.MatrixOfInertia()

        self.weight = vprop.Mass()
        self.cg = vprop.CentreOfMass()

        for i,j in zip(range(3), range(3)):
            self.I[i, j] = inertia.Value(i+1, j+1)

        print(self.weight)

    def create_wing(l_in, l_out, height, th):

        edge1 = CreateEdge().from_2_points(gp_Pnt(0,0,0), gp_Pnt(0,0,l_in))
        edge2 = CreateEdge().from_2_points(gp_Pnt(0,0,0), gp_Pnt(0, height, 0))
        edge3 = CreateEdge().from_2_points(gp_Pnt(0, height, 0), gp_Pnt(0, height, l_out))
        edge4 = CreateEdge().from_2_points(gp_Pnt(0, 0, l_in), gp_Pnt(0, height, l_out))
        contour = CreateWire().from_elements([edge1, edge2, edge3, edge4])
        face = CreateFace().from_contour(contour)
        shell = CreateExtrusion().surface(face, gp_Vec(th, 0, 0))
        shape = CreateTopology().make_solid(shell)

        return shape


wings=Wings('wings')
wings.run_once()