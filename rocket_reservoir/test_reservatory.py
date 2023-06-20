import numpy as np
from reservatory import Reservatory
from cosapp.drivers import RungeKutta

class TestReservatory:

    def test_fuel(self):

        sys = Reservatory('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 3., 'p_out' : 0., 'm_p' : 0.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 16.)

    def test_flight(self):

        sys = Reservatory('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 0., 'p_out' : 3., 'm_p' : 15.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 1.)


test_res = TestReservatory()
test_res.test_fuel()
print("Test fuel passed!")
test_res.test_flight()
print("Test flight passed!")

