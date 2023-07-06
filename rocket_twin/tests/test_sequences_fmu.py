import numpy as np
from rocket_twin.systems import Station
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder

class TestSequencesFMU:

    def test_sequence_fmu(self):

        sys = Station('sys', fmu_path="rocket_twin/systems/control/controller.fmu")
        driver = sys.add_driver(RungeKutta(order=4,time_interval=[0, 15], dt=0.01))
        init = {'g_tank.weight_p' : 10.,
                'rocket.tank.weight_p' : 0.}
        values = {'g_tank.w_out_max' : 1.,
                  'rocket.tank.w_out_max' : 0.5,
                  'rocket.engine.force_max' : 100.}
        driver.set_scenario(init=init, values=values)
        driver.add_recorder(DataFrameRecorder(includes=['rocket.dyn.a']), period=1.)
        sys.run_drivers()

        data=driver.recorder.export_data()
        print(data)

        np.testing.assert_allclose(sys.rocket.dyn.a, 40., atol=10**(-1))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5., atol=10**(-2))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0., atol=10**(-2))