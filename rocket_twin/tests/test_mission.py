import numpy as np

from rocket_twin.drivers.mission import Mission
from rocket_twin.systems import Station


class TestMission:
    """Tests for the mission driver."""

    def test_run_once(self):
        sys = Station("sys")
        dt = 0.1

        init = {
            "g_tank.weight_p": "g_tank.weight_max",
            "rocket.force_command": 0.0,
            "rocket.tank.weight_p": 0.0,
            "rocket.tank.w_out_max": 0.0,
            "g_tank.w_command": 1.0,
            "g_tank.w_in": 0.0,
            "g_tank.w_out_max": 3.0,
        }

        stop = "rocket.tank.weight_p <= 0."

        includes = ["rocket.a", "g_tank.weight", "rocket.tank.weight_p"]

        sys.add_driver(
            Mission("mission", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        data = sys.drivers["mission"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.a, 40.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (-10))


tm = TestMission()
tm.test_run_once()
