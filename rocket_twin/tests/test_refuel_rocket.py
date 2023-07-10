import numpy as np

from rocket_twin.drivers.fueling_rocket import FuelingRocket
from rocket_twin.systems import Station


class TestFuelingRocket:
    """Tests for the FuelingRocket driver."""

    def test_run_once(self):
        sys = Station("sys")
        dt = 0.1

        init = {
            "rocket.tank.weight_p": 0.0,
            "controller.cos_control.wr_temp": 0.0,
            "controller.cos_control.f_temp": 0.0,
            "controller.cos_control.wg_temp": 1.0,
            "g_tank.weight_p": "g_tank.weight_max",
            "g_tank.w_in": 0.0,
            "g_tank.w_out_max": 3.0,
        }

        stop = "rocket.tank.weight_p >= rocket.tank.weight_max"

        includes = ["rocket.a", "g_tank.weight", "rocket.tank.weight_p"]

        sys.add_driver(
            FuelingRocket("fr", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.a, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 5.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (-10))
