from cosapp.base import System

class GroundReservatory(System):

    def setup(self):

        self.add_inward('p_in', 0., desc="Fuel income rate", unit='kg/s')
        self.add_inward('p_out', 1., desc="Fuel exit rate", unit='kg/s')

        self.add_inward('w_max', 10., desc="Maximum capacity", unit='kg')

        self.add_transient('w', der='p_in - p_out', desc="Fuel rate of change")

