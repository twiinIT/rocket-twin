#main
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from rocket_twin.systems import Ground
import numpy as np

sys = Ground("ground", stations = ["station"])

dt = 1.
T = 50.

init = {"station.g_tank.fuel.weight_p" : 5.,
        "station.rocket.stage_1.tank.fuel.weight_p" : 0.,
        "station.fueling" : True,
        "station.rocket.flying" : False,
       }

driver = sys.add_driver(RungeKutta(order=4, dt=dt))
solver = driver.add_child(NonLinearSolver('solver'))
driver.time_interval = (0, T)
driver.set_scenario(init=init)

includes = ["a_station","v_station", "r_station"]

driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

sys.run_drivers()
data = driver.recorder.export_data()

print(data)