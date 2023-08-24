import numpy as np
from cosapp.drivers import NonLinearSolver

from rocket_twin.systems import Station


class TestStation:
    """Tests for the station model."""

    def test_run_once(self):
        sys = Station("sys")

        sys.run_once()

    def test_NLS(self):
        sys = Station("sys")
        sys.add_driver(NonLinearSolver("solver"))
        sys.run_drivers()
