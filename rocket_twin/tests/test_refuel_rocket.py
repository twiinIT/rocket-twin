import numpy as np

from rocket_twin.drivers.fueling_rocket import FuelingRocket
from rocket_twin.systems import Station


class TestFuelingRocket:
    """Tests for the FuelingRocket driver."""

    def test_run_once(self):
        sys = Station("sys")
        sys.g_tank.weight_p = sys.g_tank.weight_max
        sys.rocket.tank.weight_p = 0.0
        w_out = 3.0
        dt = 0.1

        sys.add_driver(FuelingRocket("fr", w_out=w_out, dt=dt, owner=sys))

        sys.run_drivers()

        data = sys.drivers["fr"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.dyn.a, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 5.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (-10))


test_fr = TestFuelingRocket()
test_fr.test_run_once()
print("Test run_once passed!")
