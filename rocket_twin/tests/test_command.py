import numpy as np
from rocket_twin.systems import Clock
from cosapp.drivers import RungeKutta

class TestClock:

    def test_time(self):

        sys = Clock('sys')
        sys.add_driver(RungeKutta(order=4,time_interval=[0, 15], dt=1.))
        sys.run_drivers()

        np.testing.assert_allclose(sys.time_var, 15., atol=10**(-4))

