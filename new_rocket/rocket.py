from cosapp.base import System

from fins import Fins
from nose import Nose
from tube import Tube
from engine import Engine
from tank import Tank
from rocket_aero import RocketAero
from rocket_geom import RocketGeom
from dynamics import Dynamics
from kinematics import Kinematics

class Rocket(System):

    def setup(self):

        self.add_child(Fins('fins'))
        self.add_child(Nose('nose'))
        self.add_child(Tube('tube'))
        self.add_child(Engine('engine'))
        self.add_child(Tank('tank'))
        self.add_child(RocketAero('aero'))
        self.add_child(RocketGeom('geom'))
        self.add_child(Dynamics('dyn'))
        self.add_child(Kinematics('kin'))
        
        self.connect(self.fins, self.aero, ['Ar_fins', 'Cna_1', 'y_mac', 'RGC', 'RDIF', 'RFIF', 'delta', 'R_fins', 'Cd_fins', 'Cna_fins', 'Aw_fins', 'tf', 'c_bar', 'Xcp_fins', 'Lf'])
        self.connect(self.nose, self.aero, ['Ar_nose', 'Cd_nose', 'Cna_nose', 'Aw_nose', 'L_nose', 'Xcp_nose'])
        self.connect(self.tube, self.aero, ['R_tube', 'L_tube', 'Aw_tube'])