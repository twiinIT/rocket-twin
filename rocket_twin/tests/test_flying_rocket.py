import numpy as np

from rocket_twin.drivers.vertical_flying_rocket import VerticalFlyingRocket
from rocket_twin.systems.ground import Ground


class TestVerticalFlyingRocket:
    def test_run_once(self):
        sys = Ground("sys")
        sys.g_tank.weight_p = 0.0
        sys.rocket.tank.weight_p = sys.rocket.tank.weight_max
        w_out = 3.0
        dt = 0.1

        sys.add_driver(VerticalFlyingRocket("vfr", w_out=w_out, dt=dt, owner=sys))

        sys.run_drivers()

        data = sys.drivers["vfr"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.dyn.a, 40.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 0.0, atol=10 ** (-10))


test_vfr = TestVerticalFlyingRocket()
test_vfr.test_run_once()
print("Test run_once passed!")
