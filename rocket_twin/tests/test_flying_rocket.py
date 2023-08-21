import numpy as np

from rocket_twin.drivers.vertical_flying_rocket import VerticalFlyingRocket
from rocket_twin.systems import Station


class TestVerticalFlyingRocket:
    """Tests for the VerticalFlyingRocket driver."""

    def test_run_once(self):
        sys = Station("sys")
        sys.rocket.stage_1.tank.fuel.weight_p = 5.0
        dt = 0.1

        init = {
            "rocket.flying": True,
            "controller.w_temp": 0.0,
            "rocket.stage_1.controller.w_temp": 1.0,
            "rocket.stage_1.tank.fuel.weight_p": 5.0,
            "rocket.stage_1.tank.fuel.w_out_max": 3.0,
            "g_tank.w_in": 0.0,
            "g_tank.fuel.weight_p": 0.0,
        }

        stop = "rocket.stage_1.tank.weight_prop <= 0."

        includes = ["rocket.a", "g_tank.weight", "rocket.stage_1.tank.weight_prop"]

        sys.add_driver(
            VerticalFlyingRocket("vfr", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        data = sys.drivers["vfr"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(acel[-2], 65.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_prop, 0.0, atol=10 ** (-10))
