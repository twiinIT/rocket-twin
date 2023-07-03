import numpy as np

from rocket_twin.systems.physics import Dynamics


class TestDynamics:
    """Tests for the dynamics model."""

    def test_is_on(self):
        sys = Dynamics("sys", forces=["F"], weights=["w"], centers=["cg"])
        sys.F = 100.0
        sys.w = 5.0
        sys.cg = 3.0
        sys.flight = True

        sys.run_once()

        np.testing.assert_allclose(sys.a, 10.0, atol=10 ** (-10))

    def test_is_off(self):
        sys = Dynamics("sys", forces=["F"], weights=["w"], centers=["cg"])
        sys.F = 10.0
        sys.w = 5.0
        sys.cg = 3.0
        sys.flight = False

        sys.run_once()

        np.testing.assert_allclose(sys.a, 0.0, atol=10 ** (-10))

    def test_cg(self):
        sys = Dynamics("sys", weights=["w1", "w2"], centers=["c1", "c2"])

        sys.c1 = 2.0
        sys.c2 = 3.0
        sys.w1 = 1.0
        sys.w2 = 4.0

        sys.run_once()

        np.testing.assert_allclose(sys.center, 2.8, atol=10 ** (-10))
