import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder

from rocket_twin.systems import Rocket, Station


class TestStage:

    sys = Station("sys", n_stages=3)

    def test_run_once(self):
        sys2 = Rocket("sys")

        sys2.run_once()

    def test_fuel(self):

        init = {
            "g_tank.fuel.weight_p": 20.0,
            "g_tank.fuel.w_out_max": 1.0,
        }

        includes = [
            "g_tank.weight_prop",
            "rocket.weight_prop_1",
            "rocket.weight_prop_2",
            "rocket.weight_prop_3",
        ]

        driver = self.sys.add_driver(RungeKutta("rk", order=4, dt=1))
        solver = driver.add_child(NonLinearSolver('solver'))
        driver.time_interval = (0, 20)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

        self.sys.run_drivers()

        data = driver.recorder.export_data()
        data1 = data.drop(["Section", "Status", "Error code", "rocket.weight_prop_2", "rocket.weight_prop_3"], axis=1)
        data2 = data.drop(["Section", "Status", "Error code", "g_tank.weight_prop", "rocket.weight_prop_1"], axis=1)

        print(data1)
        print(data2)

        np.testing.assert_allclose(self.sys.rocket.weight_prop_1, 5.0, rtol=10 ** (-1))
        np.testing.assert_allclose(self.sys.rocket.weight_prop_2, 5.0, rtol=10 ** (-1))
        np.testing.assert_allclose(self.sys.rocket.weight_prop_3, 5.0, rtol=10 ** (-1))
        np.testing.assert_allclose(self.sys.g_tank.weight_prop, 5.0, atol=10 ** (-2))

    def test_flight(self):

        init = {
            "rocket.stage_1.tank.fuel.w_out_max": 1.0,
            "rocket.stage_2.tank.fuel.w_out_max": 1.0,
            "rocket.stage_3.tank.fuel.w_out_max": 1.0,
        }

        stop = "rocket.weight_prop_3 == 0."

        includes = [
            "g_tank.weight_prop",
            "rocket.weight_prop_1",
            "rocket.weight_prop_2",
            "rocket.weight_prop_3",
        ]

        driver = self.sys.add_driver(RungeKutta("rk", order=4, dt=1))
        solver = driver.add_child(NonLinearSolver('solver'))
        driver.time_interval = (20, 40)
        driver.set_scenario(init=init, stop=stop)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

        self.sys.run_drivers()

        data = driver.recorder.export_data()
        data1 = data.drop(["Section", "Status", "Error code", "rocket.weight_prop_2", "rocket.weight_prop_3"], axis=1)
        data2 = data.drop(["Section", "Status", "Error code", "g_tank.weight_prop", "rocket.weight_prop_1"], axis=1)

        print(data1)
        print(data2)

        #acel = np.asarray(data["rocket.a"])
        #print(data)

        np.testing.assert_allclose(self.sys.rocket.weight_prop_1, 0.0, rtol=10 ** (-1))
        np.testing.assert_allclose(self.sys.rocket.weight_prop_2, 0.0, rtol=10 ** (-1))
        np.testing.assert_allclose(self.sys.rocket.weight_prop_3, 0.0, rtol=10 ** (-1))
        np.testing.assert_allclose(self.sys.rocket.geom.weight, 4.0, rtol=10 ** (-1))
        #np.testing.assert_allclose(acel[-2], 40.0, atol=10 ** (-2))
