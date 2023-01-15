from cosapp.base import System


class Mass(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
    
        #System constants
        self.add_inward('m0', 100., desc = "Rocket's Initial Mass", unit = 'kg')
        self.add_inward('qp', 10., desc = "Engine's Propulsive Debt", unit = 'kg/s')
        self.add_inward('qi', 0., desc = "Engine's Inertial Debt", unit = 'kg/s')
        self.add_inward('dmdt', 0., desc = "Mass' Rate of Change", unit = 'kg/s')
        
        #System transients
        self.add_transient('m', der = "dmdt", desc = "Rocket Mass")
        
        self.add_outward('m_out', 100., desc = "Rocket Mass", unit = 'kg')
        
    def compute(self):
        self.dmdt = - 1 if self.time <= 3.6 else 0
        self.m_out = self.m
    
    