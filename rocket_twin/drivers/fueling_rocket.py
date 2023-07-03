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

    def __init__(
        self,
        name: str,
        owner: Optional["System"] = None,
        init: Optional[dict] = None,
        stop: Optional[str] = None,
        dt: Optional[float] = 0.1,
        includes: Optional[list[str]] = None,
        **kwargs
    ):
        super().__init__(name, owner, **kwargs)

        # Fueling:
        self.rk = self.add_driver(RungeKutta("rk", owner=owner, order=4, dt=dt))
        self.rk.time_interval = (self.owner.time, 1000000.0)
        self.solver = self.rk.add_child(NonLinearSolver("solver"))

        self.rk.set_scenario(init=init, stop=stop)
        self.rk.add_recorder(
            DataFrameRecorder(includes=includes, hold=True),
            period=dt,
        )
        self.data = None

    def compute(self):
        self.data = self.rk.recorder.export_data()
