from cosapp.base import System
import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from cosapp.tools import problem_viewer

class BasicEventSystem(System):

    def setup(self):

        self.add_event('e', trigger = "time > 5.")

class Ball(System):

    def setup(self):

        self.add_child(Dynamics('Dyn'))
        self.add_child(Kinematics('Kin'))
        self.add_child(BasicEventSystem('Sys'))

        self.connect(self.Dyn, self.Kin, ['a'])

    def transition(self):

        if self.Sys.e.present:

            self.pop_child('Dyn')
            self.add_child(Dynamics_2('Dyn2'))
            self.connect(self.Dyn2, self.Kin, ['a'])


class Dynamics_2(System):

    def setup(self):

        self.add_outward('a', 1., desc = "Ball acceleration", unit = 'm/s**2')

    def compute(self):

        self.a = 0.

class Dynamics(System):

    def setup(self):

        self.add_inward('a0', 2., desc = "Ball acceleration", unit = 'm/s**2')
        self.add_outward('a', 1., desc = "Ball acceleration", unit = 'm/s**2')

    def compute(self):

        self.a = self.a0

class Kinematics(System):

    def setup(self):

        self.add_inward('a', 1., desc = "Ball acceleration", unit = 'm/s**2')
        self.add_inward('r_out', 0., desc = "Ball Position", unit = 'm')

        self.add_transient('v', der = 'a', desc = "Ball Velocity")
        self.add_transient('r', der = 'v', desc = "Ball Position")


#####MAIN FUNCTION

#Time-step
dt = 0.1

#Create System
ball = Ball('ball')

#Add RungeKutta driver
driver = ball.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 10)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))


# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Kin.r', 'Kin.v', 'Kin.a']),
    period=1,
)

#Initial conditions and constants

driver.set_scenario(
    init = {
        'Kin.r' : 0.,
        'Kin.v' : 0.
    })


ball.run_drivers()

# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
traj = np.asarray(data['Kin.r'].tolist())
velo = np.asarray(data['Kin.v'].tolist())
acel = np.asarray(data['Kin.a'].tolist())

print(time)
print(traj)
print(velo)
print(acel)