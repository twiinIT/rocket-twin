import numpy as np

from rocket_twin.systems.physics import Dynamics


class TestDynamics:
    """Tests for the dynamics model."""

    def test_is_on(self):
        sys = Dynamics("sys", forces=["F"], weights=["w"])
        sys.F = np.array([0.0, 0.0, 100.0])
        sys.w = 5.0

        sys.run_once()

        np.testing.assert_allclose(sys.a, np.array([0.0, 0.0, 10.0]), atol=10 ** (-10))

    def test_is_off(self):
        sys = Dynamics("sys", forces=["F"], weights=["w"])
        sys.F = np.array([0.0, 0.0, 10.0])
        sys.w = 5.0

        sys.run_once()

        np.testing.assert_allclose(sys.a, np.array([0.0, 0.0, -8.0]), atol=10 ** (-10))
