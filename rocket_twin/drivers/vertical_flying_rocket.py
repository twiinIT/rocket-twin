from cosapp.drivers import Driver, RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from cosapp.systems import System
from typing import Optional


class VerticalFlyingRocket(Driver):

    def __init__(self,
                 name: str,
                 flux,
                 dt,
                 owner: Optional['System'] = None,
                 **kwargs):

        super().__init__(name, owner, **kwargs)

        #Fueling:
        self.rk = self.add_driver(RungeKutta("rk", owner=owner, order=4, dt=dt))
        self.rk.time_interval = (0., 1.0)
        self.solver = self.rk.add_child(NonLinearSolver("solver"))
        self.time_end = 0.

        init = {'rocket.dyn.switch' : True,
                'g_tank.p_in' : 0.,
                'pipe.pi_in' : 0.,
                'pipe.pi_out' : 0.,
                'rocket.tank.p_out' : flux,
                }
        
        stop = 'rocket.tank.w_p <= 0.' 

        self.rk.set_scenario(init=init, stop=stop)
        self.rk.add_recorder(DataFrameRecorder(includes=['rocket.dyn.a', 'g_tank.w', 'rocket.tank.w_p'], hold=True), period=dt)
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