import numpy as np
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.GProp import GProp_GProps
from pyoccad.create import CreateCone, CreateCylinder

from rocket_twin.systems import OCCGeometry


class TestGeometry:
    """Tests for the geometry model."""
    def test_structure(self):

        sys = OCCGeometry("sys", shapes=["cylinder_s", "cone_s"], properties=["cylinder", "cone"])

        center_cyl = gp_Pnt(0, 0, 0)
        dir_cyl = gp_Vec(0, 0, 20)
        center_con = gp_Pnt(0, 0, 20)
        dir_con = gp_Pnt(0, 0, 10)
        radius = 3.0
        dens_cyl = 10.0
        dens_con = 20.0

        cylinder_s = CreateCylinder.from_base_and_dir(center_cyl, dir_cyl, radius)
        cone_s = CreateCone.from_base_and_dir(center_con, dir_con, radius)

        cylinder = GProp_GProps()
        cone = GProp_GProps()
        vprop = GProp_GProps()
        vprop2 = GProp_GProps()
        brepgprop.VolumeProperties(cylinder_s, vprop)
        brepgprop.VolumeProperties(cone_s, vprop2)
        cylinder.Add(vprop, dens_cyl)
        cone.Add(vprop2, dens_con)

        sys.cylinder_s = cylinder_s
        sys.cone_s = cone_s
        sys.cylinder = cylinder
        sys.cone = cone

        sys.run_once()
        print(sys.weight)
        print(sys.cg)

        np.testing.assert_allclose(sys.weight, 7539.822, atol=10 ** (-1))
        np.testing.assert_allclose(sys.cg, 13.125, atol=10 ** (-1))

        np.testing.assert_allclose(sys.I[0, 0], 431725.5164, atol=10 ** (-2))
        np.testing.assert_allclose(sys.I[1, 1], 431725.5164, atol=10 ** (-2))
        np.testing.assert_allclose(sys.I[2, 2], 30536.2806, atol=10 ** (-2))
