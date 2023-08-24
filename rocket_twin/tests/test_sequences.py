import numpy as np

from rocket_twin.systems import Station
from rocket_twin.utils import run_sequences


class TestSequences:
    """Tests for command through sequences."""

    sys = Station("sys")

    def test_init(self):

        seq = [
            {
                "name": "start",
                "init": {"g_tank.fuel.weight_p": 10.0},
                "type": "static",
            }
        ]

        run_sequences(self.sys, seq)

        np.testing.assert_allclose(
            self.sys.g_tank.weight_prop, self.sys.g_tank.weight_max, atol=10 ** (-6)
        )
        np.testing.assert_allclose(self.sys.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (-6))
        np.testing.assert_allclose(self.sys.rocket.a, 0.0, atol=10 ** (-6))

    def test_fuel(self):

        seq = [
            {
                "name": "fuel",
                "type": "transient",
                "init": {"g_tank.fuel.w_out_max": 1.0},
                "dt": 0.1,
                "stop": "rocket.stage_1.tank.weight_prop == rocket.stage_1.tank.weight_max",
            }
        ]

        run_sequences(self.sys, seq)

        np.testing.assert_allclose(
            self.sys.g_tank.weight_prop,
            self.sys.g_tank.weight_max - self.sys.rocket.stage_1.tank.weight_max,
            atol=10 ** (-6),
        )
        np.testing.assert_allclose(
            self.sys.rocket.stage_1.tank.weight_prop,
            self.sys.rocket.stage_1.tank.weight_max,
            atol=10 ** (-6),
        )
        np.testing.assert_allclose(self.sys.rocket.a, 0.0, atol=10 ** (-6))

    def test_flight(self):

        seq = [
            {
                "name": "flight",
                "type": "transient",
                "init": {
                    "rocket.stage_1.tank.fuel.w_out_max": 0.5,
                },
                "dt": 0.1,
                "stop": "rocket.stage_1.tank.weight_prop == 0",
            }
        ]

        run_sequences(self.sys, seq)

        data = self.sys.drivers["rk"].recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(
            self.sys.g_tank.weight_prop,
            self.sys.g_tank.weight_max - self.sys.rocket.stage_1.tank.weight_max,
            atol=10 ** (-6),
        )
        np.testing.assert_allclose(self.sys.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (-6))
        np.testing.assert_allclose(acel[-2], 2.5, atol=10 ** (-6))

    def test_all(self):

        sys2 = Station("sys2")

        seq = [
            {
                "name": "start",
                "init": {"g_tank.fuel.weight_p": 10.0},
                "type": "static",
            },
            {
                "name": "fuel",
                "type": "transient",
                "init": {"g_tank.fuel.w_out_max": 1.0},
                "dt": 0.1,
                "stop": "rocket.stage_1.tank.weight_prop == rocket.stage_1.tank.weight_max",
            },
            {
                "name": "flight",
                "type": "transient",
                "init": {
                    "rocket.stage_1.tank.fuel.w_out_max": 0.5,
                },
                "dt": 0.1,
                "stop": "rocket.stage_1.tank.weight_prop == 0",
            },
        ]

        run_sequences(sys2, seq)

        data = sys2.drivers["rk"].recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(
            sys2.g_tank.weight_prop,
            sys2.g_tank.weight_max - sys2.rocket.stage_1.tank.weight_max,
            atol=10 ** (-6),
        )
        np.testing.assert_allclose(sys2.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (-6))
        np.testing.assert_allclose(acel[-2], 2.5, atol=10 ** (-6))
