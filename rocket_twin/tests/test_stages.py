import numpy as np

from rocket_twin.systems import Stage
from cosapp.drivers import RungeKutta

class TestStage:

    def test_single_stage(self):

        sys = Stage('sys')
        init = {"tank.weight_p" : "tank.weight_max"}
        values = {"controller.w_temp" : 1., "tank.w_out_max" : 1.}
        stop = "tank.weight_p == 0."

        driver = sys.add_driver(RungeKutta(order=4, dt = 0.1))
        driver.time_interval = (0, 10)
        driver.set_scenario(init = init, values=values, stop=stop)
        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 2., atol=10**(-1))
        np.testing.assert_allclose(sys.cg, 1., atol=10**(-1))
        