from cosapp.base import System
from cosapp.drivers import Driver, RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from rocket import Rocket

import numpy as np

dt = 0.1
T = 5

rocket = Rocket('rocket')

driver = rocket.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, T)

driver.add_child(NonLinearSolver("solver", factor=1.0))

driver.add_recorder(DataFrameRecorder(includes=['a', 'reserv.m_p', 'center']), period=dt)

init = {
    'reserv.m_s' : 1.,
    'reserv.m_p' : 3.
}

stop = 'reserv.m_p <= 0'

driver.set_scenario(init=init, stop=stop)

rocket.run_drivers()

data = driver.recorder.export_data()
data = data.drop(["Section", "Status", "Error code"], axis=1)
time = np.asarray(data["time"])
acel = np.asarray(data["a"].tolist())
m_prop = np.asarray(data["reserv.m_p"].tolist())
xcg = np.asarray(data['center'].tolist())

print(acel)
print(m_prop)
print(xcg)
