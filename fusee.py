from cosapp.base import System
import numpy as np


#Modèle d'une fusée simple sans atmosphère en 1D

class Mass(System):
	def setup(self):
		self.add_inward("m_f", 2.)
		self.add_inward("Dm", 1.)
		self.add_inward("m_g")
		self.add_outward("m")
		self.add_outward("Dm_computed")
		self.add_event('endCombustion', trigger="m <= m_f")
		self.add_outward_modevar('end', False)

	def transition(self):
		if self.endCombustion.present:
			self.end = True

	def compute(self):
		self.Dm_computed = self.Dm * (not self.end)
		self.m = self.m_g * (not self.end) + self.m_f - self.time * self.Dm_computed

class Dynamics(System):
	def setup(self):
		self.add_inward("end")
		self.add_inward("Dm_computed")
		self.add_inward("m")
		self.add_inward("u")
		self.add_inward("g")
		self.add_outward("force")
		self.add_outward("a")
	
	def compute(self):
		self.force = self.m * self.g - self.Dm_computed * self.u
		self.a = self.force / self.m 



class Fusee(System):
	def setup(self):
		self.add_child(Mass('mass'), pulling = "Dm")
		self.add_child(Dynamics("dynamics"), pulling = ["u", "g", "a"])
		self.g = -9.81
		self.u = -100. #m/s

		self.add_transient('v', der='a')
		self.add_transient('z', der='v')
		self.connect(self.mass, self.dynamics, {"m" : "m", "Dm_computed" : "Dm_computed"})
	

		self.exec_order = ['mass', 'dynamics']



from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder



fusee = Fusee("fusee")
fusee.mass.m_g = 7.0

fusee2 = Fusee("fusee2")
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

plt.plot(time, traj, 'r', label = "Masse de gaz : 1 kg")
plt.plot(time2, traj2, 'b', label = "Masse de gaz : 7 kg")

plt.title("Trajectoire d'une fusée de 2kg à vide, débit massique de 1.0kg/s,\n soumise à son poids et à une force de poussée")
plt.xlabel("time"),
plt.ylabel("altitude")

plt.legend()
plt.show()