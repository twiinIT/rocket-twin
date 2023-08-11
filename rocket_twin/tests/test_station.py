from rocket_twin.systems import Station
from cosapp.drivers import NonLinearSolver
import numpy as np

class TestStation:

    def test_run_once(self):
        sys = Station('sys')

        sys.run_once()

    def test_NLS(self):
        sys = Station('sys')
        sys.add_driver(NonLinearSolver('solver'))
        sys.run_drivers()