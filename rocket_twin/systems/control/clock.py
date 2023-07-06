from cosapp.base import System

class Clock(System):

    def setup(self):

        #Transient to ensure the system is visited in every time step
        self.add_transient('x', der='1')
        self.add_outward('time_var', 0., desc="Command time")

    def compute(self):

        self.time_var = self.time