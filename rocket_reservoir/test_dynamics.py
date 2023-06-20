import numpy as np
from dynamics import Dynamics

class TestDynamics:

    def test_run_once(self):

        sys = Dynamics('sys', forces=['F'], weights=['w'])
        sys.F = 100.
        sys.w = 5.

        sys.run_once()

        np.testing.assert_allclose(sys.a, 10.)


test_dyn = TestDynamics()
test_dyn.test_run_once()
print("Test run_once passed!")
