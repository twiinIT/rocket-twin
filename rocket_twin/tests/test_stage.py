import numpy as np
from rocket_twin.systems import Rocket

class TestStage:

    def test_run_once(self):
        sys = Rocket("sys")

        sys.run_once()