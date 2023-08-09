import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Tank


class TestTank:
    """Tests for the tank model."""

    def test_fuel(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"w_in": 3.0, "fuel.w_out_max": 0.0, "weight_p": 0.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight_p, 15.0, atol=10 ** (-10))

    def test_flight(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"w_in": 0.0, "fuel.w_out_max": 3.0, "weight_p": 15.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight_p, 0.0, atol=10 ** (-10))

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
            "weight_p": 6.0,
            "w_in": 0.0,
            "fuel.w_out_max": 1.0,
        }

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.props.Mass(), 0.86 * np.pi + 1.0, atol=10 ** (-2))
