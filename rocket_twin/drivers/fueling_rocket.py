from typing import Optional

from cosapp.drivers import Driver, NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.systems import System


class FuelingRocket(Driver):
    """Driver that simulates the fueling of a rocket.
    
    Inputs
    ------
    name: string,
        the name of the driver
    w_out [kg/s]: float,
        mass flow of fuel exiting the ground tank
    dt [s]: float,
        integration time step
    owner: System,
        the system that owns the driver

    Outputs
    ------
    """
    def __init__(self, name: str, w_out, dt, owner: Optional["System"] = None, **kwargs):
        super().__init__(name, owner, **kwargs)

        # Fueling:
        self.rk = self.add_driver(RungeKutta("rk", owner=owner, order=4, dt=dt))
        self.rk.time_interval = (0.0, 1.0)
        self.solver = self.rk.add_child(NonLinearSolver("solver"))
        self.time_end = 0.0

        init = {
            "rocket.dyn.switch": False,
            "rocket.tank.w_out_temp": 0.0,
            "g_tank.w_in": 0.0,
            "g_tank.w_out_temp": w_out,
        }

        stop = "rocket.tank.weight_p >= rocket.tank.weight_max"

        self.rk.set_scenario(init=init, stop=stop)
        self.rk.add_recorder(
            DataFrameRecorder(
                includes=["rocket.dyn.a", "g_tank.weight", "rocket.tank.weight_p"], hold=True
            ),
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
