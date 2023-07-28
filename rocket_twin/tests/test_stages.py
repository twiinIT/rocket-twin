import numpy as np
from cosapp.drivers import EulerExplicit, RungeKutta
from cosapp.recorders import DataFrameRecorder

from rocket_twin.systems import Station, Stage


class TestStage:
    def test_single_stage(self):

        sys = Stage("sys")
        init = {"tank.weight_p": "tank.weight_max"}
        values = {"controller.w_temp": 1.0, "tank.w_out_max": 1.0}
        stop = "tank.weight_p == 0."

        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 10)
        driver.set_scenario(init=init, values=values, stop=stop)
        sys.run_drivers()

        np.testing.assert_allclose(sys.weight, 2.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.cg, 1.0, atol=10 ** (-2))

    def test_two_stages(self):

        sys = Station("sys", n_stages=2)
        init = {
            "rocket.stage_1.weight_p": "rocket.stage_1.weight_max",
            "rocket.stage_2.weight_p": "rocket.stage_2.weight_max",
            "rocket.stage_1.controller.w_temp": 1.0,
        }

        driver = sys.add_driver(RungeKutta("rk", order=4, dt=0.1))
        driver.time_interval = (0, 10)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=["rocket.dyn.weight"]), period=1.0)
        sys.run_drivers()

        data = driver.recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)
        print(data)

        np.testing.assert_allclose(sys.rocket.dyn.weight, 2.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.rocket.dyn.center, 1.0, atol=10 ** (-2))

    def test_n_stages(self, n=3):

        sys = Station("sys", n_stages=n)
        init = {"rocket.stage_1.controller.w_temp": 1.0}
        for i in range(n):
            init[f"rocket.stage_{i + 1}.weight_p"] = f"rocket.stage_{i + 1}.weight_max"


        driver = sys.add_driver(EulerExplicit("rk", dt=0.1))
        driver.time_interval = (0, 16)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=["rocket.dyn.weight"]), period=1.0)
        sys.run_drivers()

        data = driver.recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)
        print(data)

        np.testing.assert_allclose(sys.rocket.dyn.weight, 3.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.rocket.dyn.center, 1.0, atol=10 ** (-2))
