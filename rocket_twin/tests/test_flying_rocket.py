import numpy as np

from rocket_twin.drivers.vertical_flying_rocket import VerticalFlyingRocket
from rocket_twin.systems import Station


class TestVerticalFlyingRocket:
    """Tests for the VerticalFlyingRocket driver."""

    def test_run_once(self):
        sys = Station("sys")
        sys.rocket.tank.weight_p = sys.rocket.tank.weight_max
        dt = 0.1

        init = {
            "rocket.flying": 1.0,
            "controller.w_temp": 0.0,
            "rocket.controller.w_temp": 1.0,
            "rocket.weight_p": "rocket.tank.weight_max",
            "rocket.tank.w_out_max": 3.0,
            "g_tank.w_in": 0.0,
            "g_tank.weight_p": 0.0,
        }

        stop = "rocket.tank.weight_p <= 0."

        includes = ["rocket.a", "g_tank.weight", "rocket.tank.weight_p"]

        sys.add_driver(
            VerticalFlyingRocket("vfr", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        # data = sys.drivers["vfr"].data
        # data = data.drop(["Section", "Status", "Error code"], axis=1)
        # print(data)

        np.testing.assert_allclose(sys.rocket.a, 290.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 0.0, atol=10 ** (-10))
