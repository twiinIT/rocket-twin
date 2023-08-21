import numpy as np

from rocket_twin.drivers.fueling_rocket import FuelingRocket
from rocket_twin.systems import Station


class TestFuelingRocket:
    """Tests for the FuelingRocket driver."""

    def test_run_once(self):
        sys = Station("sys")
        dt = 0.1

        init = {
            "rocket.stage_1.tank.fuel.weight_p": 0.0,
            "rocket.stage_1.controller.w_temp": 0.0,
            "controller.w_temp": 1.0,
            "g_tank.fuel.weight_p": 10.0,
            "g_tank.w_in": 0.0,
            "g_tank.fuel.w_out_max": 3.0,
        }

        stop = "rocket.stage_1.tank.weight_prop >= rocket.stage_1.tank.weight_max"

        includes = ["rocket.a", "g_tank.weight", "rocket.stage_1.tank.weight_prop"]

        sys.add_driver(
            FuelingRocket("fr", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.a, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.stage_1.tank.weight_prop, 5.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_prop, 5.0, atol=10 ** (-10))
