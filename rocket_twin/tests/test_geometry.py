import numpy as np
from OCC.Core.gp import gp_Pnt, gp_Vec
from pyoccad.create import CreateCone, CreateCylinder

from rocket_twin.systems import Geometry


class TestGeometry:
    def test_structure(self):

        sys = Geometry("sys", shapes=["cylinder", "cone"], densities=["dens_cyl", "dens_con"])

        center_cyl = gp_Pnt(0, 0, 0)
        dir_cyl = gp_Vec(0, 0, 20)
        center_con = gp_Pnt(0, 0, 20)
        dir_con = gp_Pnt(0, 0, 10)
        radius = 3.0
        dens_cyl = 10.0
        dens_con = 20.0

        cylinder = CreateCylinder.from_base_and_dir(center_cyl, dir_cyl, radius)
        cone = CreateCone.from_base_and_dir(center_con, dir_con, radius)
        print(type(cylinder))

        sys.cylinder = cylinder
        sys.cone = cone
        sys.dens_cyl = dens_cyl
        sys.dens_con = dens_con

        sys.run_once()
        print(sys.weight)
        print(sys.cg)
        np.testing.assert_allclose(sys.weight, 7539.822, atol=10 ** (-1))
        np.testing.assert_allclose(sys.cg, 13.125, atol=10 ** (-1))
