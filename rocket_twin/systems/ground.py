from cosapp.base import System

from rocket_twin.systems import Pipe, Rocket, Tank


class Ground(System):
    def setup(self):
        self.add_child(Rocket("rocket"))
        self.add_child(Pipe("pipe"))
        self.add_child(Tank("g_tank"))

        self.connect(self.g_tank.outwards, self.pipe.inwards, {'p_out' : 'p_in'})
        self.connect(self.pipe.outwards, self.rocket.inwards, {'p_out' : 'p_in'})

        self.g_tank.w_max = 10.
        self.rocket.tank.w_p = 0.

        self.exec_order = ["pipe", "g_tank", "rocket"]

        #Design methods
        dm = self.add_design_method('start')
        dm.add_unknown('g_tank.w_p')
        dm.add_equation('g_tank.w_p == g_tank.w_max')

        #dm = self.add_design_method('fuel')
        #dm.add_unknown('pipe.p')
        #dm.add_target('rocket.tank.w_p')

        #dm = self.add_design_method('flight')
        #dm.add_unknown('rocket.tank.p_out')
        #dm.add_target('rocket.tank.w_p')
