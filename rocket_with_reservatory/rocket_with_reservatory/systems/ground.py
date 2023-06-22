from cosapp.base import System
from rocket_with_reservatory.systems import Rocket, Pipe, GroundReservatory

class Ground(System):

    def setup(self):

        self.add_child(Rocket('rocket'))
        self.add_child(Pipe('pipe'))
        self.add_child(GroundReservatory('g_res'))

        self.connect(self.pipe.outwards, self.g_res.inwards, {'p_in' : 'p_out'})
        self.connect(self.pipe.outwards, self.rocket.inwards, {'p_out' : 'p_in'})

        self.exec_order = ['pipe', 'g_res', 'rocket']