from cosapp.base import System, Port
from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
import numpy as np
import matplotlib.pyplot as plt
from cosapp.drivers import NonLinearSolver, RunSingleCase


class connections_pipes(Port):

    def setup(self):
        self.add_variable('P',1.0e5, desc = 'pressure value', unit = 'Pa')
        self.add_variable('Q',1., desc='mass flow rate', unit = 'kg/s')
        #self.add_variable('k', desc='loss coefficient', unit = 'N*s/(kg*m**2)')


class Pipe(System):

    def setup(self):

        self.add_input(connections_pipes,'IN')
        self.add_inward('k',0.05)


        self.add_output(connections_pipes,'OUT')
        #self.add_outward('dp',2*10e5)
        self.add_outward('dp',0.0)

        # design methods
        self.add_inward('dp_design',2e5)
        self.add_design_method('kd').add_unknown('k').add_equation(' dp == dp_design')  #allow the solver to modify the inward value
        #init
        #self.IN.P = 5e5

    def compute(self):
        
        self.dp = self.k*(self.IN.Q)**2 
        self.OUT.P = self.IN.P -self.dp 
        self.OUT.Q = self.IN.Q

h2 = Pipe('H2')
h2.IN.Q = 2.
h2.IN.P = 3.0e5
#h2.run_once()

solver = h2.add_driver(NonLinearSolver('solver'))

# Add design point
case = solver.add_child(RunSingleCase('case'))

# Define case conditions
#case.set_values({
#    'k_design': 2*10e5,
#})

case.design.extend(h2.design_methods['kd'])  # activate design method 'kd' of system `h2`

h2.run_drivers()

print(
    f"{h2.OUT.P = }",
    f"{h2.IN.P = }",
    f"{h2.k = }",
    f"{h2.IN.Q = }",
    sep="\n" )



class HeadPipe(System):
    def setup(self):

        self.add_child(Pipe('pipe1'), pulling={'IN':'IN','k':'k1'})
        self.add_child(Pipe('pipe2'), pulling = {'OUT':'OUT','k':'k2'})
        self.connect(self.pipe1.OUT, self.pipe2.IN)

        self.add_inward('dp_design',1.0e5)
        self.add_design_method('kdd').add_unknown(['k1','k2']).add_equation([' IN.P - OUT.P == dp_design','pipe1.dp == 2*pipe2.dp'])





h = HeadPipe('head_pipe')

h.IN.P = 5*10**5   
h.IN.Q = 2 


h.run_once()


print(
    f"{h.OUT.P = }",
    f"{h.IN.P = }",
    f"{h.pipe2.k = }",
    sep="\n" )

