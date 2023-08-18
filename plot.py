import numpy as np
from rocket_twin.systems import Station
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
import matplotlib.pyplot as plt

sys = Station('sys', n_stages=3)
T = 20.

init = {'g_tank.fuel.weight_p' : 20.,
        'g_tank.fuel.w_out_max' : 1.,
        'controller.w_temp' : 1.}

values = {'rocket.stage_1.tank.geom.height' : 1.4,
          'rocket.stage_2.tank.geom.height' : 1.2}
        
includes = ["g_tank.weight_prop", "rocket.weight_prop_1", "rocket.weight_prop_2", "rocket.weight_prop_3", "rocket.geom.weight"]

driver = sys.add_driver(RungeKutta('rk', order=4, dt = 1))
driver.time_interval = (0, T)
driver.set_scenario(init=init, values = values)
driver.add_recorder(DataFrameRecorder(includes=includes), period=1.)

sys.run_drivers()

data = driver.recorder.export_data()
data = data.drop(["Section", "Status", "Error code"], axis=1)

time = np.asarray(data['time'])
fuel1 = np.asarray(data["rocket.weight_prop_1"])
fuel2 = np.asarray(data["rocket.weight_prop_2"])
fuel3 = np.asarray(data["rocket.weight_prop_3"])
fuelg = np.asarray(data["g_tank.weight_prop"])
mass = np.asarray(data["rocket.geom.weight"])

plt.plot(time, fuel1, label="Stage 1 fuel")
plt.plot(time, fuel2, label="Stage 2 fuel")
plt.plot(time, fuel3, label="Stage 3 fuel")
plt.plot(time, fuelg, label="Ground fuel")
plt.plot(time, mass, label="Rocket mass")
plt.xlabel("Time (s)")
plt.ylabel("Fuel mass (kg)")
plt.title("Fuel mass over time")
plt.legend()
plt.show()

sys.drivers.clear()

init = {'rocket.stage_1.controller.w_temp' : 1.}

values = {'rocket.stage_1.tank.fuel.w_out_max' : 1.,
          'rocket.stage_2.tank.fuel.w_out_max' : 1.,
          'rocket.stage_3.tank.fuel.w_out_max' : 1.}
        
includes = ["g_tank.weight_prop", "rocket.weight_prop_1", "rocket.weight_prop_2", "rocket.weight_prop_3", "rocket.geom.weight"]

driver = sys.add_driver(RungeKutta('rk', order=4, dt = 1))
driver.time_interval = (T, 2*T)
driver.set_scenario(init=init, values = values)
driver.add_recorder(DataFrameRecorder(includes=includes), period=1.)

sys.run_drivers()

data = driver.recorder.export_data()
data = data.drop(["Section", "Status", "Error code"], axis=1)

time = np.asarray(data['time'])
fuel1 = np.asarray(data["rocket.weight_prop_1"])
fuel2 = np.asarray(data["rocket.weight_prop_2"])
fuel3 = np.asarray(data["rocket.weight_prop_3"])
fuelg = np.asarray(data["g_tank.weight_prop"])
mass = np.asarray(data["rocket.geom.weight"])

plt.plot(time, fuel1, label="Stage 1 fuel")
plt.plot(time, fuel2, label="Stage 2 fuel")
plt.plot(time, fuel3, label="Stage 3 fuel")
plt.plot(time, fuelg, label="Ground fuel")
plt.plot(time, mass, label="Rocket mass")
plt.xlabel("Time (s)")
plt.ylabel("Fuel mass (kg)")
plt.title("Fuel mass over time")
plt.legend()
plt.show()