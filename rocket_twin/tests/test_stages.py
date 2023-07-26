import numpy as np
from cosapp.drivers import EulerExplicit, RungeKutta
from cosapp.recorders import DataFrameRecorder

from rocket_twin.systems import Rocket, Stage


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

        sys = Rocket("sys", n_stages=2)
        init = {
            "stage_1.weight_p": "stage_1.weight_max",
            "stage_2.weight_p": "stage_2.weight_max",
            "stage_1.controller.w_temp": 1.0,
        }
        stop = "stage_2.weight_p == 0."

        driver = sys.add_driver(RungeKutta("rk", order=4, dt=0.1))
        driver.time_interval = (0, 10)
        driver.set_scenario(init=init, stop=stop)
        driver.add_recorder(DataFrameRecorder(includes=["dyn.center"]), period=1.0)
        sys.run_drivers()

        data = driver.recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)
        print(data)

        np.testing.assert_allclose(sys.dyn.weight, 2.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.dyn.center, 1.0, atol=10 ** (-2))

    def test_n_stages(self, n=3):

        sys = Rocket("sys", n_stages=n)
        init = {"stage_1.controller.w_temp": 1.0}
        for i in range(n):
            init[f"stage_{i + 1}.weight_p"] = f"stage_{i + 1}.weight_max"
        stop = f"stage_{n}.weight_p == 0."

        driver = sys.add_driver(EulerExplicit("rk", dt=0.1))
        driver.time_interval = (0, 16)
        driver.set_scenario(init=init, stop=stop)
        driver.add_recorder(DataFrameRecorder(includes=["dyn.weight"]), period=1.0)
        sys.run_drivers()

        data = driver.recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)
        print(data)

        np.testing.assert_allclose(sys.dyn.weight, 3.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.dyn.center, 1.0, atol=10 ** (-2))
