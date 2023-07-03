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
            "rocket.engine.switch": True,
            "rocket.tank.weight_p": "rocket.tank.weight_max",
            "rocket.tank.w_out_temp": 3.0,
            "g_tank.w_in": 0.0,
            "g_tank.weight_p": 0.0,
            "g_tank.is_open": False,
        }

        stop = "rocket.tank.weight_p <= 0."

        includes = ["rocket.dyn.a", "g_tank.weight", "rocket.tank.weight_p"]

        sys.add_driver(
            VerticalFlyingRocket("vfr", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        data = sys.drivers["vfr"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.dyn.a, 40.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 0.0, atol=10 ** (-10))


"""init = {
            "rocket.dyn.switch": True,
            "g_tank.w_in": 0.0,
            "pipe.is_open": False,
            "rocket.tank.w_out_temp": w_out,
        }

        stop = "rocket.tank.weight_p <= 0."""

# ["rocket.dyn.a", "g_tank.weight", "rocket.tank.weight_p"]
