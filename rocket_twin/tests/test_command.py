import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Clock


class TestClock:
    def test_time(self):

        sys = Clock("sys")
        sys.add_driver(RungeKutta(order=4, time_interval=[0, 15], dt=1.0))
        sys.run_drivers()

        np.testing.assert_allclose(sys.time_var, 15.0, atol=10 ** (-4))
