import numpy as np
from cosapp.drivers import NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.utils import swap_system

from rocket_twin.systems import (
    RocketControllerFMU,
    StageControllerFMU,
    Station,
    StationControllerFMU,
)


class TestControllerFMU:
    """Tests for the FMU controller."""

    def test_controller_fmu(self):

        n_stages = 3

        model_path = r"systems\control\station_controller.mo"
        model_name = "station_controller"

        model_path_r = r"systems\control\rocket_controller.mo"
        model_name_r = "rocket_controller"

        model_path_s = r"systems\control\stage_controller.mo"
        model_name_s = "stage_controller"

        sys = Station("sys", n_stages=n_stages)
        swap_system(
            sys.controller,
            StationControllerFMU("controller", model_path=model_path, model_name=model_name),
        )
        swap_system(
            sys.rocket.controller,
            RocketControllerFMU(
                "controller", n_stages=n_stages, model_path=model_path_r, model_name=model_name_r
            ),
        )
        for i in range(1, n_stages + 1):
            swap_system(
                sys.rocket[f"stage_{i}"].controller,
                StageControllerFMU("controller", model_path=model_path_s, model_name=model_name_s),
            )

        driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 35], dt=1.0))
        driver.add_child(NonLinearSolver("solver"))
        init = {
            "g_tank.fuel.weight_p": 20.0,
            "rocket.stage_1.tank.fuel.weight_p": 0.0,
            "rocket.stage_2.tank.fuel.weight_p": 0.0,
            "rocket.stage_3.tank.fuel.weight_p": 0.0,
        }
        values = {
            "g_tank.fuel.w_out_max": 1.0,
            "time_int": 5.0,
            "rocket.stage_1.tank.fuel.w_out_max": 1.0,
            "rocket.stage_2.tank.fuel.w_out_max": 1.0,
            "rocket.stage_3.tank.fuel.w_out_max": 1.0,
        }
        driver.set_scenario(init=init, values=values)
        driver.add_recorder(
            DataFrameRecorder(includes=["rocket.a"]),
            period=1.0,
        )
        sys.run_drivers()
        data = driver.recorder.export_data()

        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(sys.rocket.geom.weight, 4.0, atol=10 ** (0))
        np.testing.assert_allclose(acel[-2], 40.0, rtol=0.1)
