import numpy as np

from rocket_twin.systems import RocketGeom


class TestRocketGeom:
    """Tests for the rocket geometry model."""

    def test_run_once(self):
        sys = RocketGeom("sys", centers=["c1", "c2"], weights=["w1", "w2"])

        sys.c1 = 2.0
        sys.c2 = 3.0
        sys.w1 = 1.0
        sys.w2 = 4.0

        sys.run_once()

        np.testing.assert_allclose(sys.center, 2.8, atol=10 ** (-10))


test_geom = TestRocketGeom()
test_geom.test_run_once()
print("Test run_once passed!")
