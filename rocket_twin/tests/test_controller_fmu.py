import numpy as np
import pytest
from cosapp.drivers import RungeKutta
from cosapp.utils import swap_system

from rocket_twin.systems import ControllerFMU, Station


class TestControllerFMU:
    @pytest.mark.skip(reason="Multi-stage rocket not yet adapted to fmu controller.")
    def test_controller_fmu(self):

        model_path = r"systems\control\controller.mo"
        model_name = "controller"

        model_path_r = r"systems\control\rocket_controller.mo"
        model_name_r = "rocket_controller"

        sys = Station("sys")
        swap_system(
            sys.controller,
            ControllerFMU("controller", model_path=model_path, model_name=model_name),
        )
        swap_system(
            sys.rocket.stage_1.controller,
            ControllerFMU("controller", model_path=model_path_r, model_name=model_name_r),
        )

        sys.connect(sys.controller.inwards, sys.rocket.inwards, ["weight_max", "weight_p"])
        sys.rocket.stage_1.connect(
            sys.rocket.stage_1.controller.inwards,
            sys.rocket.stage_1.tank.inwards,
            ["weight_max", "weight_p"],
        )

        driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 18], dt=0.01))
        init = {"g_tank.weight_p": 10.0, "rocket.stage_1.tank.weight_p": 0.0}
        values = {
            "g_tank.w_out_max": 1.0,
            "rocket.stage_1.tank.w_out_max": 0.5,
            "controller.time_int": 3.0,
            "rocket.stage_1.controller.time_int": 3.0,
        }
        driver.set_scenario(init=init, values=values)
        # driver.add_recorder(DataFrameRecorder(includes=["rocket.a", "rocket.dyn.a"]), period=1.0)

        sys.run_drivers()
        # data = driver.recorder.export_data()
        # data = data.drop(["Section", "Status", "Error code"], axis=1)
        # print(data)

        np.testing.assert_allclose(sys.rocket.a, 40.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.rocket.stage_1.tank.weight_p, 0.0, atol=10 ** (0))
