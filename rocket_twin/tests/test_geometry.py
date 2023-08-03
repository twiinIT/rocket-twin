import numpy as np
from rocket_twin.systems import Geometry
from pyoccad.create import CreateCylinder, CreateCone
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps

class TestGeometry:

    def test_structure(self):

        sys = Geometry('sys', shapes=['cylinder', 'cone'], densities=['dens_cyl', 'dens_con'])

        center_cyl = gp_Pnt(0, 0, 0)
        dir_cyl = gp_Vec(0, 0, 20)
        center_con = gp_Pnt(0, 0, 20)
        dir_con = gp_Pnt(0, 0, 10)
        radius = 3.
        dens_cyl = 10.
        dens_con = 20.

        cyl_model = CreateCylinder.from_base_and_dir(center_cyl, dir_cyl, radius)
        con_model = CreateCone.from_base_and_dir(center_con, dir_con, radius)

        cylinder = GProp_GProps()
        brepgprop.VolumeProperties(cyl_model, cylinder)

        cone = GProp_GProps()
        brepgprop.VolumeProperties(con_model, cone)

        sys.cylinder = cylinder
        sys.cone = cone
        sys.dens_cyl = dens_cyl
        sys.dens_con = dens_con

        sys.run_once()
        print(sys.weight)
        print(sys.cg)
        np.testing.assert_allclose(sys.weight, 1., atol=10**(-10))