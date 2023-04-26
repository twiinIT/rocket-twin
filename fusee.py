from cosapp.base import System
import numpy as np


#Modèle d'une fusée simple sans atmosphère en 1D

class Mass(System):
	def setup(self):
		self.add_inward("m_f", 2., desc="Rocket mass without propellant", unit="kg")
		self.add_inward("Dm", 1., desc="Initial mass flow rate", unit="kg/s")
		self.add_inward("m_g", desc="Propellant mass", unit="kg")
		self.add_outward("m", desc="Mass during flight", unit="kg")
		self.add_outward("Dm_computed", desc="Mass flow rate during flight", unit="kg/s")
		self.add_event('endCombustion', trigger="m <= m_f")
		self.add_outward_modevar('end', False, desc="True if there is no more propellant", unit="")

	def transition(self):
		if self.endCombustion.present:
			self.end = True

	def compute(self):
		self.Dm_computed = self.Dm * (not self.end)
		self.m = self.m_g * (not self.end) + self.m_f - self.time * self.Dm_computed

class Dynamics(System):
	def setup(self):
		self.add_inward("Dm_computed",  desc="Mass flow rate during flight", unit="kg/s")
		self.add_inward("m", desc="Mass during flight", unit="kg")
		self.add_inward("u", desc="Ejection speed of the propellant", unit="m/s")
		self.add_inward("g", desc="Gravity", unit="m/s**2")
		self.add_outward("force", desc="Applied force", unit="N")
		self.add_outward("a", desc="Rocket acceleration", unit="m/s**2")
	
	def compute(self):
		self.force = self.m * self.g - self.Dm_computed * self.u
		self.a = self.force / self.m 



class Rocket(System):
	def setup(self):
		self.add_inward('g', -9.81, desc="Gravity", unit="m/s**2")
		self.add_inward('u', -100., desc="Ejection speed of the propellant", unit="m/s")

		self.add_child(Mass('mass'), pulling = "Dm")
		self.add_child(Dynamics("dynamics"), pulling = ["u", "g", "a"])

		self.add_transient('v', der='a')
		self.add_transient('z', der='v')
		self.connect(self.mass, self.dynamics, {"m" : "m", "Dm_computed" : "Dm_computed"})

		self.exec_order = ['mass', 'dynamics']



from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder



fusee = Rocket("fusee")
fusee.mass.m_g = 7.0

fusee2 = Rocket("fusee2")
fusee2.mass.m_g = 1.0


driver = fusee.add_driver(RungeKutta(order=2, dt=.01))
driver.time_interval = (0,30)

driver2 = fusee2.add_driver(RungeKutta(order=2, dt=.01))
driver2.time_interval = (0,30)

driver.add_recorder(DataFrameRecorder(includes=['z', 'v', 'a']), period=.05,)
driver2.add_recorder(DataFrameRecorder(includes=['z', 'v', 'a']), period=.05,)

driver.set_scenario(
	init = {
		'z': 0.,
		'v': 0.,
	},
	stop = 'z <= 0.' #On arrete la simulation quand la fusée tombe au sol
	)
driver2.set_scenario(
	init = {
		'z': 0.,
		'v': 0.,
	},
	stop = 'z <= 0.' #On arrete la simulation quand la fusée tombe au sol
	)

fusee.run_drivers()
fusee2.run_drivers()

data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
traj = np.asarray(data['z'].tolist())

data2 = driver2.recorder.export_data()
data2 = data2.drop(['Section', 'Status', 'Error code'], axis=1)
time2 = np.asarray(data2['time'])
traj2 = np.asarray(data2['z'].tolist())

length = traj.size

import matplotlib.pyplot as plt

plt.plot(time, traj, 'r', label = "Masse de gaz : 7 kg")
plt.plot(time2, traj2, 'b', label = "Masse de gaz : 1 kg")

plt.title("Altitude en fonction du temps de la simulation 1D")
plt.xlabel("time"),
plt.ylabel("altitude")

plt.legend()
plt.show()