import numpy as np
from cosapp.drivers import RungeKutta

from rocket_twin.systems import Station


class TestSequencesFMU:
    def test_sequence_fmu(self):

        model_path = r"C:\\Users\\Lucs\\Documents\\Polytechnique\\PSC\\rocket-twin\\rocket_twin\\systems\\control\\controller.mo"
        model_name = "controller"
        sys = Station("sys", model_path=model_path, model_name=model_name)
        driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 15], dt=0.01))
        init = {"g_tank.weight_p": 10.0, "rocket.tank.weight_p": 0.0}
        values = {
            "g_tank.w_out_max": 1.0,
            "rocket.tank.w_out_max": 0.5,
            "rocket.engine.force_max": 100.0,
        }
        driver.set_scenario(init=init, values=values)
        sys.run_drivers()

        np.testing.assert_allclose(sys.rocket.dyn.a, 40.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (0))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (0))
