import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Tank


class TestTank:
    """Tests for the tank model."""

    def test_fuel(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"w_in": 3.0, "w_out_max": 0.0, "weight_p": 0.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 16.0, atol=10 ** (-10))

    def test_flight(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"w_in": 0.0, "w_out_max": 3.0, "weight_p": 15.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 1.0, atol=10 ** (-10))
