import numpy as np
from rocket_twin.systems import Tank
from cosapp.drivers import RungeKutta

class TestTank:

    def test_fuel(self):

        sys = Tank('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 3., 'p_out' : 0., 'w_p' : 0.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 16., atol=10**(-10))

    def test_flight(self):

        sys = Tank('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 0., 'p_out' : 3., 'w_p' : 15.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 1., atol=10**(-10))


test_res = TestTank()
test_res.test_fuel()
print("Test fuel passed!")
test_res.test_flight()
print("Test flight passed!")

