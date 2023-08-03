from cosapp.base import System
from pyoccad.create import CreateCylinder, Create
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
import numpy as np

class Tube(System):

    def setup(self):

        # Geometric parameters
        self.add_inward('radius', 1., desc="radius", unit='m')
        self.add_inward('length', 1., desc="length", unit='m')

        # Pyoccad model
        shape = CreateCylinder().from_base_and_dir(gp_Pnt(0, 0, 0), gp_Vec(0, 0, self.length), self.radius)
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