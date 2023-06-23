from typing import Optional

from cosapp.drivers import Driver, NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.systems import System


class FuellingRocket(Driver):
    def __init__(self, name: str, flux, dt, owner: Optional["System"] = None, **kwargs):
        super().__init__(name, owner, **kwargs)

        # Fueling:
        self.rk = self.add_driver(RungeKutta("rk", owner=owner, order=4, dt=dt))
        self.rk.time_interval = (0.0, 1.0)
        self.solver = self.rk.add_child(NonLinearSolver("solver"))
        self.time_end = 0.0

        init = {
            "rocket.dyn.switch": False,
            "rocket.tank.p_out": 0.0,
            "g_tank.p_in": 0.0,
            "pipe.pi_in": flux,
            "pipe.pi_out": flux,
        }

        stop = "rocket.tank.w_p >= rocket.tank.w_max"

        self.rk.set_scenario(init=init, stop=stop)
        self.rk.add_recorder(
            DataFrameRecorder(includes=["rocket.dyn.a", "g_tank.w", "rocket.tank.w_p"], hold=True),
            period=dt,
        )
        self.data = None

    def compute(self):
        pass

    def _precompute(self):
        self.rk.time_interval = (self.owner.time, 1000000.0)
        super()._precompute()

    def _postcompute(self) -> None:
        self.time_end = self.rk.time
        self.data = self.rk.recorder.export_data()
        return super()._postcompute()
