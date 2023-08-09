import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Wings


class TestWings:
    """Tests for the wings model."""

    def test_geometry(self):
        sys = Wings("sys")

        sys.n = 2
        sys.l_in = 1.0
        sys.l_out = 1.0
        sys.width = 1.0
        sys.th = 0.1
        sys.radius = 0.0
        sys.rho = 10.0
        sys.pos = 0.0

        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        sys.run_drivers()

        np.testing.assert_allclose(sys.props.Mass(), 2.0, atol=10 ** (-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 0.5, atol=10 ** (-2))

        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().X(), 1.01 / 6, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Y(), 5 / 6, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Z(), 4.01 / 6, atol=10 ** (-2)
        )
