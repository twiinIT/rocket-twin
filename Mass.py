from cosapp.base import System


class Mass(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('m0', 1., desc = "Rocket's Initial Mass")
        self.add_inward('I0', 1.475e-3, desc = "Rocket's Initial Inertia Moment")
        self.add_inward('m', 1., desc = "Rocket Mass")
        
        #Mass outputs
        self.add_outward('Dm', 1, desc = "Rocket Mass' Rate of Change")
        self.add_outward('I', self.I0, desc = "Rocket's Inertia Moment")

        #Events
        self.add_event('noMoreEngine', trigger="time >= 3.6") #voir thrust.txt

        #Transients
        self.add_transient('m', der='-Dm')
        
    def transition(self):
        if self.noMoreEngine.present:
            self.Dm = 0
        
    def compute(self):
        self.I = self.I0 * self.m/self.m0