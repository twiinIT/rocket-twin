from cosapp.base import System

from Ports import VelPort

import numpy as np


class Wind(System):
	def setup(self):
		self.add_output(VelPort, "v_wind")
		self.add_inward('r', np.zeros(3), desc='rocket position in earth referential', unit='m')

	def compute(self):
		self.v_wind.val = wind(self.r[2])

def wind(alt):
	if alt>100 and alt<200:
		return np.array([0,1,0])
	else:
		return np.zeros(3)