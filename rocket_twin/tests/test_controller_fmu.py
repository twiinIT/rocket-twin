import os

import numpy as np
from cosapp.drivers import RungeKutta
from maintenance.utils import swap_system

import rocket_twin.systems.control
from rocket_twin.systems import Controller, Station


class TestControllerFMU:
    def test_controller_fmu(self):

        fmu_path = os.path.join(rocket_twin.systems.control.__path__[0], "controller.fmu")

        fmu_path_r = os.path.join(rocket_twin.systems.control.__path__[0], "rocket_controller.fmu")

        sys = Station("sys")
        swap_system(sys.controller, Controller("controller", fmu_path=fmu_path))
        swap_system(
            sys.rocket.controller,
            Controller("controller", fmu_path=fmu_path_r),
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
