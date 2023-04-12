from cosapp.base import System

import numpy as np

class Mass(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Mass is in the Rocket's referential")
        
        #Rocket inputs
        self.add_inward('m', 1.639, desc = "Rocket's Mass")
        self.add_inward('m0', 1.639, desc = "Rocket's Initial Mass")

        self.add_inward('I0_geom', np.array([10., 100., 100.]), desc = "Rocket's Initial Inertia Moment/mass")

        #Mass outputs
        self.add_outward('I', self.I0_geom*self.m, desc = "Rocket's Inertia Moment")
        self.add_outward('Dm', (0.16 - 0.084)/1, desc = "Rocket Mass' Rate of Change")
        self.add_outward('m_out', 0, desc= "Rocket's mass", unit='kg')


        #Events
        self.add_event('noMoreEngine', trigger="time >= 0.9") #voir thrust.txt

        #Transients
        self.add_transient('m', der='-Dm',)
        
    def transition(self):
        if self.noMoreEngine.present:
            self.Dm = 0
        
    def compute(self):
        self.I = self.I0_geom * self.m / self.m0
        self.m_out = self.m