from cosapp.base import System
from dynamics import Dynamics
from engine import Engine
from reservatory import Reservatory
from rocket_geom import RocketGeom

class Rocket(System):

    def setup(self):

        self.add_child(Engine('engine'))
        self.add_child(Reservatory('reserv'), pulling=['p_in'])
        self.add_child(RocketGeom('geom', centers=['engine', 'reservatory'], weights=['weight_eng', 'weight_res']), pulling=['center'])
        self.add_child(Dynamics('dyn', forces=['thrust'], weights=['weight_eng', 'weight_res']), pulling=['a'])

        self.connect(self.engine.outwards, self.geom.inwards, {'cg' : 'engine', 'weight' : 'weight_eng'})
        self.connect(self.reserv.outwards, self.geom.inwards, {'cg' : 'reservatory', 'weight' : 'weight_res'})
        self.connect(self.engine.outwards, self.dyn.inwards, {'force' : 'thrust', 'weight' : 'weight_eng'})
        self.connect(self.reserv.outwards, self.dyn.inwards, {'weight' : 'weight_res'})

        self.exec_order = ['engine', 'reserv', 'geom', 'dyn']