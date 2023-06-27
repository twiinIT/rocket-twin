import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Tank


class TestTank:
    def test_fuel(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"p_in": 3.0, "flux": 0.0, "w_p": 0.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 16.0, atol=10 ** (-10))

    def test_flight(self):
        sys = Tank("sys")
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"p_in": 0.0, "flux": 3.0, "w_p": 15.0}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 1.0, atol=10 ** (-10))


test_res = TestTank()
test_res.test_fuel()
print("Test fuel passed!")
test_res.test_flight()
print("Test flight passed!")
