from cosapp.base import System

from atmosphere import Atmosphere
from gravity import Gravity
from reservatory import Reservatory
from rocket import Rocket
from trajectory import Trajectory

class Earth(System):

    def setup(self):

        self.add_child(Gravity('grav'))
        self.add_child(Atmosphere('atmo'))
        self.add_child(Trajectory('traj'))
        self.add_child(Rocket('rocket'))
        self.add_child(Reservatory('reserv'))