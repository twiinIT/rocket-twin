from cosapp.base import System

class Pipe(System):

    def setup(self):

        self.add_outward('p_in', 1., desc="Fuel income rate", unit='kg/s')
        self.add_outward('p_out', 1., desc="Fuel exit rate", unit='kg/s')