import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Engine


class TestEngine:
    """Tests for the engine model."""
    def test_run_once(self):
        sys = Engine("sys")

        sys.run_once()

    def test_geom(self):
        sys = Engine("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {
            "geom.base_radius": 3.0,
            "geom.top_radius": 1.0,
            "geom.height": 2.0,
            "geom.rho": 15 / (13 * np.pi),
            "geom.pos": 0.0,
        }

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.props.Mass(), 10.0, atol=10 ** (-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 0.692, atol=10 ** (-2))

        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().X(), 16.553, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Y(), 16.553, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Z(), 27.923, atol=10 ** (-2)
        )

    def test_perfo(self):
        sys = Engine("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"perfo.w_out": 10.0, "perfo.isp": 20.0, "perfo.g_0": 10.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.force, 2000.0, atol=10 ** (-5))
