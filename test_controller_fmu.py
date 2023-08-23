import numpy as np
from cosapp.drivers import NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.utils import swap_system

from rocket_twin.systems import ControllerFMU, RocketControllerFMU, Station


class TestControllerFMU:
    def test_controller_fmu(self):

        n_stages = 3

        model_path = r"systems\control\controller.mo"
        model_name = "controller"

        model_path_r = r"systems\control\rocket_controller.mo"
        model_name_r = "rocket_controller"

        sys = Station("sys", n_stages=n_stages)
        swap_system(
            sys.controller,
            ControllerFMU("controller", model_path=model_path, model_name=model_name),
        )
        swap_system(
            sys.rocket.controller,
            RocketControllerFMU("controller", n_stages=n_stages, model_path=model_path_r, model_name=model_name_r),
        )
        for i in range(1, n_stages + 1):
            swap_system(
                sys.rocket[f"stage_{i}"].controller,
                ControllerFMU("controller", model_path=model_path, model_name=model_name)
            )

        driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 40], dt=0.1))
        solver = driver.add_child(NonLinearSolver("solver"))
        init = {"g_tank.fuel.weight_p": 20.0,
                "rocket.stage_1.tank.fuel.weight_p": 0.0,
                "rocket.stage_2.tank.fuel.weight_p": 0.0,
                "rocket.stage_3.tank.fuel.weight_p": 0.0}
        values = {
            "g_tank.fuel.w_out_max": 1.0,
            "rocket.controller.time_int": 5.0,
            "rocket.stage_1.tank.fuel.w_out_max": 1.,
            "rocket.stage_2.tank.fuel.w_out_max": 1.,
            "rocket.stage_3.tank.fuel.w_out_max": 1.,
        }
        driver.set_scenario(init=init, values=values)
        driver.add_recorder(
            DataFrameRecorder(includes=["rocket.weight_prop_3", "rocket.geom.weight", "rocket.a"]),
            period=1.0,
        )
        sys.run_drivers()
        data = driver.recorder.export_data()
        data1 = data.drop(["Section", "Status", "Error code", "rocket.a"], axis=1)
        data2 = data.drop(["Section", "Status", "Error code", "rocket.geom.weight", "rocket.weight_prop_3"], axis=1)

        print(data1)
        print(data2)

        np.testing.assert_allclose(sys.rocket.geom.weight, 4., atol=10 ** (0))
        np.testing.assert_allclose(sys.rocket.a, 40., rtol=0.1)
        #np.testing.assert_allclose(sys.g_tank.weight_prop, 5.0, atol=10 ** (0))
        #np.testing.assert_allclose(sys.rocket.stage_1.tank.weight_prop, 0.0, atol=10 ** (0))
