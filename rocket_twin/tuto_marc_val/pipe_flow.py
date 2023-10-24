from cosapp.base import System, Port
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
import numpy as np
import matplotlib.pyplot as plt


class connections_pipes(Port):

    def setup(self):
        self.add_variable('P', desc = 'pressure value', unit = 'Pa')
        self.add_variable('Q', desc='mass flow rate', unit = 'kg/s')
        self.add_variable('k', desc='loss coefficient', unit = 'N*s/(kg*m**2)')


class Pipe(System):

    def setup(self):

        #
        self.add_input(connections_pipes,'IN')


        self.add_output(connections_pipes,'OUT')

    def compute(self):

        self.OUT.P = self.IN.k*(self.IN.Q)**2 + self.IN.P

h = System('head_pipe')
h.add_child(Pipe('pipe1'))
h.add_child(Pipe('pipe2'))

h.pipe1.IN.set_values(P = 5*10**5, Q = 1, k = 0.05)
h.pipe2.IN.set_values(k = 0.05)   #une autre manière sans avoir à faire appel au port

h.connect(h.pipe1.OUT, h.pipe2.IN, 'P')
h.connect(h.pipe1.IN, h.pipe2.IN, 'Q')

h.run_once()

print(
    f"{h.pipe2.OUT.P = }",
    f"{h.pipe1.IN.P = }",
    sep="\n" )
