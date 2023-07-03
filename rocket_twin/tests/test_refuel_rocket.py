import numpy as np

from rocket_twin.drivers.fueling_rocket import FuelingRocket
from rocket_twin.systems import Station


class TestFuelingRocket:
    """Tests for the FuelingRocket driver."""

    def test_run_once(self):
        sys = Station("sys")
        dt = 0.1

        init = {
            "rocket.engine.switch": False,
            "rocket.tank.weight_p": 0.0,
            "rocket.tank.w_out_temp": 0.0,
            "g_tank.is_open": True,
            "g_tank.weight_p": "g_tank.weight_max",
            "g_tank.w_in": 0.0,
            "g_tank.w_out_temp": 3.0,
        }

        stop = "rocket.tank.weight_p >= rocket.tank.weight_max"

        includes = ["rocket.dyn.a", "g_tank.weight", "rocket.tank.weight_p"]

        sys.add_driver(
            FuelingRocket("fr", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.dyn.a, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 5.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (-10))
