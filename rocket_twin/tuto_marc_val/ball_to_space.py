from cosapp.base import System
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
import numpy as np
import matplotlib.pyplot as plt

class Ball(System):

    def setup(self):

        #
        self.add_inward('m',10, desc = 'mass value', unit = 'kg')
        self.add_inward('F',np.array([100,100]), desc='Force value', unit = 'N')
        #self.add_inward('a0', np.array([2.,2.]), desc='acceleration value', unit='m/s**2')
        self.add_outward('a', np.zeros((2)), desc='acceleration', unit='m/s**2')

        self.add_transient('v', der='a', desc='velocity')
        self.add_transient('r', der = 'v', desc = 'position')

    def compute(self):

        self.a = self.F/self.m


ball = Ball('ball')

driver = ball.add_driver(RungeKutta(order=4,dt=0.01))
driver.time_interval=(0, 10)
driver.add_recorder(DataFrameRecorder(includes=['a','v','r']), period=0.2)
init0 = {'r' : np.zeros(2),
        'v' : np.zeros(2)}

driver.set_scenario(init=init0)

ball.run_drivers()

data = driver.recorder.export_data()

time = np.asarray(data['time'])
dist = np.asarray(data['r'].tolist())
print(dist)

plt.figure()
print(data.r[0])
plt.plot(time, dist[:,1])
print(data)
plt.show()


#gitfetch