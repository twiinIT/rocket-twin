import numpy as np
from cosapp.drivers import NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder

from rocket_twin.systems import Station


class TestControllerCosapp:
    """Tests for the cosapp controller."""
    def test_run_once(self):

        sys = Station("sys", n_stages=3)
        sys.run_once()

    def test_control(self):

        sys = Station("sys", n_stages=3)

        init = {
            "g_tank.fuel.weight_p": 20.0,
            "g_tank.fuel.w_out_max": 1.0,
            "rocket.stage_1.tank.fuel.w_out_max": 1.0,
            "rocket.stage_2.tank.fuel.w_out_max": 1.0,
            "rocket.stage_3.tank.fuel.w_out_max": 1.0,
            "time_int": 5.0,
        }

        includes = ["rocket.a"]

        driver = sys.add_driver(RungeKutta("rk", order=4, dt=1))
        solver = driver.add_child(NonLinearSolver("solver"))
        driver.time_interval = (0, 35)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

        sys.run_drivers()

        data = driver.recorder.export_data()
        acel = np.asarray(data["rocket.a"])

        np.testing.assert_allclose(sys.rocket.geom.weight, 4.0, atol=10 ** (0))
        np.testing.assert_allclose(acel[-3], 40.0, atol=0.1)
