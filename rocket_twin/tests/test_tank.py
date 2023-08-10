import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Tank


class TestTank:
    """Tests for the tank model."""

    def test_fuel(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"w_in": 3.0, "fuel.w_out_max": 0.0, "fuel.weight_p": 0.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight_prop, 15.0, atol=10 ** (-10))

    def test_flight(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"w_in": 0.0, "fuel.w_out_max": 3.0, "fuel.weight_p": 15.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight_prop, 0.0, atol=10 ** (-10))

    def test_geometry(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {
            "geom.r_int": 3.0,
            "geom.r_ext": 4.0,
            "geom.thickness": 0.1,
            "geom.height": 1.0,
            "geom.rho_struct": 0.1,
            "geom.rho_fuel": 0.2,
            "fuel.weight_p": 6.0,
            "w_in": 0.0,
            "fuel.w_out_max": 1.0,
            "geom.pos" : 0.,
        }

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.props.Mass(), 3.7017, atol=10 ** (-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 0.31413, atol=10 ** (-2))

        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().X(), 18.3849, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Y(), 18.3849, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Z(), 36.0101, atol=10 ** (-2)
        )
