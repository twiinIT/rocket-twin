import numpy as np

from rocket_twin.drivers.fueling_rocket import FuelingRocket
from rocket_twin.drivers.vertical_flying_rocket import VerticalFlyingRocket
from rocket_twin.systems import Station


class TestDrivers:
    """Tests for the FuelingRocket and VerticalFlyingRocket driver."""

    sys = Station("sys")

    def test_fuel(self):
        dt = 1.0

        init = {
            "rocket.stage_1.tank.fuel.weight_p": 0.0,
            "g_tank.fuel.weight_p": 10.0,
            "g_tank.w_in": 0.0,
            "g_tank.fuel.w_out_max": 3.0,
        }

        stop = "rocket.flying == 1."

        includes = ["rocket.a"]

        self.sys.add_driver(
            FuelingRocket("fr", owner=self.sys, init=init, stop=stop, includes=includes, dt=dt)
        )

        self.sys.run_drivers()

        data = self.sys.drivers["fr"].data
        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(acel[-2], 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(self.sys.rocket.stage_1.tank.weight_prop, 5.0, atol=10 ** (-10))
        np.testing.assert_allclose(self.sys.g_tank.weight_prop, 5.0, atol=10 ** (-10))
        np.testing.assert_allclose(self.sys.rocket.controller.flying, 1.0, atol=0.1)

    def test_flight(self):

        self.sys.drivers.clear()

        dt = 0.1

        init = {
            "rocket.stage_1.tank.fuel.w_out_max": 3.0,
            "g_tank.w_in": 0.0,
            "g_tank.fuel.weight_p": 0.0,
        }

        stop = "rocket.stage_1.tank.weight_prop <= 0."

        includes = ["rocket.a", "g_tank.weight", "rocket.stage_1.tank.weight_prop"]

        self.sys.add_driver(
            VerticalFlyingRocket(
                "vfr", owner=self.sys, init=init, stop=stop, includes=includes, dt=dt
            )
        )

        self.sys.run_drivers()

        data = self.sys.drivers["vfr"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(acel[-2], 65.0, atol=10 ** (-10))
        np.testing.assert_allclose(self.sys.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(self.sys.g_tank.weight_prop, 0.0, atol=10 ** (-10))
