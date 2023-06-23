from rocket_twin.drivers.vertical_flying_rocket import VerticalFlyingRocket
from rocket_twin.systems.ground import Ground
import numpy as np

class TestVerticalFlyingRocket:

    def test_run_once(self):

        sys = Ground('sys')
        sys.g_tank.w_p = 0.
        sys.rocket.tank.w_p = sys.rocket.tank.w_max
        flux = 3.
        dt = 0.1

        sys.add_driver(VerticalFlyingRocket('vfr', flux=flux, dt=dt, owner=sys))

        sys.run_drivers()

        data = sys.drivers['vfr'].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.a, 40., atol=10**(-10))
        np.testing.assert_allclose(sys.rocket.tank.w_p, 0., atol=10**(-10))
        np.testing.assert_allclose(sys.g_tank.w_p, 0., atol=10**(-10))

test_vfr = TestVerticalFlyingRocket()
test_vfr.test_run_once()
print("Test run_once passed!")
