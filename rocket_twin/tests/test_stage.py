import numpy as np
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder

from rocket_twin.systems import Rocket, Station


class TestStage:
    def test_run_once(self):
        sys = Rocket("sys")

        sys.run_once()

    def test_fuel(self):
        sys = Station("sys", n_stages=3)

        init = {
            "g_tank.fuel.weight_p": 20.0,
            "g_tank.fuel.w_out_max": 1.0,
            "controller.w_temp": 1.0,
        }

        includes = [
            "g_tank.weight_prop",
            "rocket.weight_prop_1",
            "rocket.weight_prop_2",
            "rocket.weight_prop_3",
        ]

        driver = sys.add_driver(RungeKutta("rk", order=4, dt=1))
        driver.time_interval = (0, 20)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.weight_prop_1, 5.0, rtol=10 ** (-1))
        np.testing.assert_allclose(sys.rocket.weight_prop_2, 5.0, rtol=10 ** (-1))
        np.testing.assert_allclose(sys.rocket.weight_prop_3, 5.0, rtol=10 ** (-1))
        np.testing.assert_allclose(sys.g_tank.weight_prop, 5.0, atol=10 ** (-2))

    def test_flight(self):

        sys = Station("sys", n_stages=3)

        init = {
            "controller.w_temp": 0.0,
            "rocket.flying": True,
            "rocket.stage_1.controller.w_temp": 1.0,
            "rocket.stage_1.tank.fuel.w_out_max": 1.0,
            "rocket.stage_1.tank.fuel.weight_p": 5.0,
            "rocket.stage_2.tank.fuel.w_out_max": 1.0,
            "rocket.stage_2.tank.fuel.weight_p": 5.0,
            "rocket.stage_3.tank.fuel.w_out_max": 1.0,
            "rocket.stage_3.tank.fuel.weight_p": 5.0,
        }

        stop = "rocket.weight_prop_3 == 0."

        includes = ["rocket.a"]

        driver = sys.add_driver(RungeKutta("rk", order=4, dt=1))
        driver.time_interval = (0, 20)
        driver.set_scenario(init=init, stop=stop)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

        sys.run_drivers()

        data = driver.recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        acel = np.asarray(data["rocket.a"])
        print(data)

        np.testing.assert_allclose(sys.rocket.weight_prop_1, 0.0, rtol=10 ** (-1))
        np.testing.assert_allclose(sys.rocket.weight_prop_2, 0.0, rtol=10 ** (-1))
        np.testing.assert_allclose(sys.rocket.weight_prop_3, 0.0, rtol=10 ** (-1))
        np.testing.assert_allclose(sys.rocket.geom.weight, 4.0, rtol=10 ** (-1))
        np.testing.assert_allclose(acel[-2], 40.0, atol=10 ** (-2))
