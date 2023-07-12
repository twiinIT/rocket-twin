import numpy as np
from cosapp.drivers import RungeKutta
from maintenance.utils import swap_system

from rocket_twin.systems import Controller, Station


class TestControllerFMU:
    def test_controller_fmu(self):

        model_path = r"systems\control\controller.mo"
        model_path_r = r"systems\control\rocket_controller.mo"
        model_name = "controller"
        model_name_r = "rocket_controller"
        sys = Station("sys")
        swap_system(
            sys.controller, Controller("controller", model_path=model_path, model_name=model_name)
        )
        swap_system(
            sys.rocket.controller,
            Controller("controller", model_path=model_path_r, model_name=model_name_r),
        )
        driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 15], dt=0.01))
        init = {"g_tank.weight_p": 10.0, "rocket.tank.weight_p": 0.0}
        values = {
            "g_tank.w_out_max": 1.0,
            "rocket.tank.w_out_max": 0.5,
        }
        driver.set_scenario(init=init, values=values)
        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.dyn.a, 40.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (0))
