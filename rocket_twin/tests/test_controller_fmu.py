import numpy as np
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.utils import swap_system

from rocket_twin.systems import ControllerFMU, Station


class TestControllerFMU:
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
            sys.rocket.controller,
            ControllerFMU("controller", model_path=model_path_r, model_name=model_name_r),
        )

        sys.connect(sys.controller.inwards, sys.rocket.inwards, ["weight_max", "weight_p"])
        sys.rocket.connect(
            sys.rocket.controller.inwards, sys.rocket.tank.inwards, ["weight_max", "weight_p"]
        )

        driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 18], dt=0.01))
        init = {"g_tank.weight_p": 10.0, "rocket.tank.weight_p": 0.0}
        values = {
            "g_tank.w_out_max": 1.0,
            "rocket.tank.w_out_max": 0.5,
            "controller.time_int": 3.0,
            "rocket.controller.time_int": 3.0,
        }
        driver.set_scenario(init=init, values=values)
        driver.add_recorder(DataFrameRecorder(includes=["rocket.a", "rocket.dyn.a"]), period=1.0)

        sys.run_drivers()
        data = driver.recorder.export_data()
        data = data.drop(["Section", "Status", "Error code"], axis=1)
        print(data)

        np.testing.assert_allclose(sys.rocket.a, 2.5, atol=10 ** (0))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (0))
