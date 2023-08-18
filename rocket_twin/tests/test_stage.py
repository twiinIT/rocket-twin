import numpy as np

from rocket_twin.systems import Rocket, Station

from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder


class TestStage:
    def test_run_once(self):
        sys = Rocket("sys")

        sys.run_once()
        print(sys.w_in_1)

    def test_fuel(self):
        sys = Station('sys', n_stages=3)

        init = {'g_tank.fuel.weight_p' : 20.,
                'g_tank.fuel.w_out_max' : 1.,
                'controller.w_temp' : 1.}
        
        includes = ["g_tank.weight_prop", "rocket.weight_prop_1", "rocket.weight_prop_2", "rocket.weight_prop_3"]

        driver = sys.add_driver(RungeKutta('rk', order=4, dt = 1))
        driver.time_interval = (0, 20)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.)

        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.weight_prop_1, 5., rtol=10**(-1))
        np.testing.assert_allclose(sys.rocket.weight_prop_2, 5., rtol=10**(-1))
        np.testing.assert_allclose(sys.rocket.weight_prop_3, 5., rtol=10**(-1))
        np.testing.assert_allclose(sys.g_tank.weight_prop, 5., atol=10**(-2))

    def test_flight(self):

        sys = Station('sys', n_stages=3)

        init = {'controller.w_temp' : 0.,
                'rocket.stage_1.controller.w_temp' : 1.,
                "rocket.stage_1.tank.fuel.w_out_max" : 1.,
                "rocket.stage_1.tank.fuel.weight_p" : 5.,
                "rocket.stage_2.tank.fuel.w_out_max" : 1.,
                "rocket.stage_2.tank.fuel.weight_p" : 5.,
                "rocket.stage_3.tank.fuel.w_out_max" : 1.,
                "rocket.stage_3.tank.fuel.weight_p" : 5.}
        
        includes = ["g_tank.weight_prop", "rocket.weight_prop_1", "rocket.weight_prop_2", "rocket.weight_prop_3"]

        driver = sys.add_driver(RungeKutta('rk', order=4, dt = 1))
        #solver = driver.add_child(NonLinearSolver('solver'))
        driver.time_interval = (0, 20)
        driver.set_scenario(init=init)
        driver.add_recorder(DataFrameRecorder(includes=includes), period=1.)

        sys.run_drivers()

        data = driver.recorder.export_data()
        data1 = data.drop(["Section", "Status", "Error code", "rocket.weight_prop_2", "rocket.weight_prop_3"], axis=1)
        data2 = data.drop(["Section", "Status", "Error code", "g_tank.weight_prop", "rocket.weight_prop_1"], axis=1)
        print(data1)
        print('\n')
        print(data2)
        print(sys.rocket.geom.weight)

        np.testing.assert_allclose(1, 2, atol=0.1)
