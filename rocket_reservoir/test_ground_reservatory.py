import numpy as np
from ground_reservatory import GroundReservatory
from cosapp.drivers import RungeKutta

class TestGroundReservatory:

    def test_filling(self):

        sys = GroundReservatory('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 1., 'p_out' : 0., 'w' : 0.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.w, 5.)

    def test_emptying(self):

        sys = GroundReservatory('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 0., 'p_out' : 1.5 , 'w' : 15.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.w, 7.5)


    def test_capacity(self):

        sys = GroundReservatory('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {'p_in' : 5., 'p_out' : 3., 'w' : 0.}
        stop = 'w >= w_max'

        driver.set_scenario(init=init, stop = stop)

        sys.run_drivers()

        np.testing.assert_allclose(sys.w, 10.)




test_g_res = TestGroundReservatory()
test_g_res.test_filling()
print("Test filling passed!")
test_g_res.test_emptying()
print("Test flight passed!")
test_g_res.test_capacity()
print("Test capacity passed!")