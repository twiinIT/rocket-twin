import numpy as np

from rocket_twin.drivers.mission import Mission
from rocket_twin.systems import Station


class TestMission:
    """Tests for the mission driver."""

    def test_run_once(self):
        sys = Station("sys")
        dt = 1.0

        init = {
            "rocket.stage_1.tank.fuel.weight_p": 0.0,
            "g_tank.fuel.weight_p": 10.0,
            "g_tank.w_in": 0.0,
            "g_tank.fuel.w_out_max": 3.0,
        }

        stop = "rocket.stage_1.tank.weight_prop <= 0."

        includes = ["rocket.a"]

        sys.add_driver(
            Mission("mission", owner=sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        sys.run_drivers()

        data = sys.drivers["mission"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(acel[-2], np.array([0.0, 0.0, 65.0]), atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_prop, 5.0, atol=10 ** (-10))
