import numpy as np

from rocket_twin.drivers.mission import Mission
from rocket_twin.systems import Station


class TestMission:
    """Tests for the mission driver."""

    def test_run_once(self):
        sys = Station("sys")
        dt = 0.1

        init = {
            "rocket.tank.fuel.weight_p": 0.0,
            "rocket.controller.w_temp": 0.0,
            "controller.w_temp": 1.0,
            "g_tank.fuel.weight_p": 10.0,
            "g_tank.w_in": 0.0,
            "g_tank.fuel.w_out_max": 3.0,
        }

        stop = "rocket.tank.weight_prop <= 0."

        includes = ["rocket.force"]

        sys.add_driver(
            Mission("mission", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        # data = sys.drivers["mission"].data
        # data = data.drop(["Section", "Status", "Error code"], axis=1)
        # print(data)

        np.testing.assert_allclose(sys.rocket.a, 65.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_prop, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_prop, 5.0, atol=10 ** (-10))
