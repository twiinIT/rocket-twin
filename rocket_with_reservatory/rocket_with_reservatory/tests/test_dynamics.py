import numpy as np
from rocket_with_reservatory.systems.physics import Dynamics

class TestDynamics:

    def test_is_on(self):

        sys = Dynamics('sys', forces=['F'], weights=['w'])
        sys.F = 100.
        sys.w = 5.
        sys.switch = True

        sys.run_once()

        np.testing.assert_allclose(sys.a, 10., atol=10**(-10))

    def test_is_off(self):

        sys = Dynamics('sys', forces=['F'], weights=['w'])
        sys.F = 100.
        sys.w = 5.
        sys.switch = False

        sys.run_once()

        np.testing.assert_allclose(sys.a, 0., atol=10**(-10))


test_dyn = TestDynamics()
test_dyn.test_is_on()
print("Test is_on passed!")
test_dyn.test_is_off()
print("Test is_off passed!")
