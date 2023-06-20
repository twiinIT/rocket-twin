from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from ground_reservatory import GroundReservatory

import numpy as np

dt = 0.1
T = 5

g_res = GroundReservatory('g_res')

driver = g_res.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, T)

driver.add_child(NonLinearSolver("solver", factor=1.0))

driver.add_recorder(DataFrameRecorder(includes=['w']), period=dt)

init = {
    'w' : 5.,
    'p_in' : 2.,
    'p_out' : 0. ,
}

stop = 'w >= w_max'

driver.set_scenario(init=init, stop=stop)

g_res.run_drivers()

data = driver.recorder.export_data()
data = data.drop(["Section", "Status", "Error code"], axis=1)
time = np.asarray(data["time"])
fuel = np.asarray(data["w"].tolist())

print(fuel)