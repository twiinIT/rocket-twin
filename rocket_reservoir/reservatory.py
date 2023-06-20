from cosapp.base import System

class Reservatory(System):

    def setup(self):

        self.add_inward('m_e', 1., desc="Empty mass", unit='kg')
        self.add_inward('m_p', 1., desc="Propellant mass", unit='kg')

        self.add_outward('m', 1., desc="Mass", unit='kg')
        self.add_outward('xcg', 1., desc="Center of gravity", unit='m')

    def compute(self):

        self.m = self.m_e + self.m_p