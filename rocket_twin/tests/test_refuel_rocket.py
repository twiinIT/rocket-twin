from rocket_twin.drivers.fuelling_rocket import FuellingRocket
from rocket_twin.systems import Ground
import numpy as np

class TestFuellingRocket:

    def test_run_once(self):

        sys = Ground('sys')
        sys.g_tank.w_p = sys.g_tank.w_max
        sys.rocket.tank.w_p = 0.
        flux = 3.
        dt = 0.1

        sys.add_driver(FuellingRocket('fr', flux=flux, dt=dt, owner=sys))

        sys.run_drivers()

        data = sys.drivers['fr'].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.a, 0., atol=10**(-10))
        np.testing.assert_allclose(sys.rocket.tank.w_p, 5., atol=10**(-10))
        np.testing.assert_allclose(sys.g_tank.w_p, 0., atol=10**(-10))

test_fr = TestFuellingRocket()
test_fr.test_run_once()
print("Test run_once passed!")
