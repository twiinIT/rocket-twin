from cosapp.base import System

from Ports import VelPort

import numpy as np

import matplotlib.pyplot as plt
import numpy.random as npr
import scipy.stats as sps





#Hauteur de l'espace contenant du vent en mètres
H = 2000
#Pas du maillage
p = 20
#Nombre de points 
N = int(H/p)

class Wind(System):
	def setup(self):
		self.add_output(VelPort, "v_wind")
		self.add_inward('r', np.zeros(3), desc='rocket position in earth referential', unit='m')

	def compute(self):
		self.v_wind.val = np.array([100, 0, 0]) #wind(self.r[2])


def wind(alt):
	alt = int(alt//p)
	w_hd = sample_wind[alt][0]
	w_vd = sample_wind[alt][1]
	w_n = sample_wind[alt][2]
	return [w_n*np.cos(w_vd)*np.cos(w_hd), -w_n*np.cos(w_vd)*np.sin(w_hd), w_n*np.sin(w_vd)*np.cos(w_hd)]
	



def sample_chol(N,q):
	sigma = np.array([[min(i,j)/q for i in range(N)] for j in range(N)])
	mu = np.array([0 for i in range(N)])
	y = sps.multivariate_normal.rvs(mean=mu, cov=sigma, size=1)
	return y

def sample_norm(N):
    y = sample_chol(N,.5)
    return abs(y)

def sample_horizontal_dir(N):
	y = sample_chol(N,200)
	origin = np.random.uniform(0,2*np.pi)
	y+=[origin for i in range(len(y))]
	return y

def sample_vertical_dir(N):
	y = sample_chol(N,500)
	return y

sample_horizontal_dir = sample_horizontal_dir(N)
sample_vertical_dir = sample_vertical_dir(N)
sample_norm = sample_norm(N)

sample_wind = [[sample_horizontal_dir[i], sample_vertical_dir[i], sample_norm[i]] for i in range(N)]

x = np.linspace(0, 2000, len(sample_wind))
plt.scatter(x,sample_horizontal_dir,color='r', marker='x', s=2)
plt.scatter(x,sample_vertical_dir ,color='b', marker='x', s=2)
plt.scatter(x,sample_norm,color='g', marker='x', s=2)
plt.show()


