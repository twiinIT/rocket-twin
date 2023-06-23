from cosapp.base import System

from rocket_twin.systems import Pipe, Rocket, Tank


class Ground(System):
    def setup(self):
        self.add_child(Rocket("rocket"))
        self.add_child(Pipe("pipe"))
        self.add_child(Tank("g_tank"))

        self.connect(self.pipe.outwards, self.g_tank.inwards, {"p_in": "p_out"})
        self.connect(self.pipe.outwards, self.rocket.inwards, {"p_out": "p_in"})

        self.exec_order = ["pipe", "g_tank", "rocket"]
