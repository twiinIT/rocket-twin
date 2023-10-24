from cosapp.base import System
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
import numpy as np

class Ball(System):

    def setup(self):

        # 
        self.add_inward('a0', np.array([2.0,2.0]), desc='acceleration value', unit='m/s**2')
        self.add_outward('a', np.array([6.0,6.0]), desc='acceleration', unit='m/s**2')

        self.add_transient('v', der='a', desc='velocity')
        self.add_transient('r', der = 'v', desc = 'position')

    def compute(self):

        self.a = self.a0


ball = Ball('ball')

driver = ball.add_driver(RungeKutta(order=4,dt=0.1))
driver.time_interval=(0, 10)
driver.add_recorder(DataFrameRecorder(includes=['a','v','r']))

ball.run_drivers()

data = driver.recorder.export_data()
print(data)

#gitfetch