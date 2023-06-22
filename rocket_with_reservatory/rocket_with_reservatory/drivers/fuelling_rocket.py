from cosapp.drivers import Driver, RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from cosapp.systems import System
from typing import Optional


class FuellingRocket(Driver):

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

        init = {'rocket.dyn.switch' : False,
                'rocket.reserv.p_out' : 0.,
                'g_res.p_in' : 0., 
                'pipe.pi_in' : flux, 
                'pipe.pi_out': flux
                }
        
        stop = 'rocket.reserv.m_p >= rocket.reserv.m_max'

        self.rk.set_scenario(init=init, stop=stop)
        self.rk.add_recorder(DataFrameRecorder(includes=['rocket.dyn.a', 'g_res.w', 'rocket.reserv.m_p'], hold=True), period=dt)
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