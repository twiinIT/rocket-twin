from cosapp.base import System

class Reservatory(System):

    def setup(self):

        self.add_inward('m_s', 1., desc="Structure mass", unit='kg')
        self.add_inward('dm_out', 1., desc="Mass consumption rate", unit='kg/s')

        self.add_transient('m_p', der='-dm_out', desc="Propellant mass")

        self.add_outward('weight', 1., desc="Weight", unit='kg')
        self.add_outward('cg', 1., desc="Center of gravity", unit='m')

    def compute(self):

        self.weight = self.m_s + self.m_p
        self.cg = 3.