from cosapp.base import System

from Rocket import Rocket
from Dynamics import Dynamics


class Earth(System):
    
    def setup(self):
        self.add_inward('referential', 'Earth', desc = "Earth is in the Earth's referential")

        self.add_child(Rocket('Rocket'), pulling = ["v", "m"]) 
        
        self.add_child(Dynamics('Dyn'), pulling = {"a" : "a", "aw" : "aw"})

        # self.add_child(Atmosphere('Atm'), pulling = ["rhosol", "Psol", "Hp", "Hd"])

        self.connect(self.Dyn, self.Rocket, ["m", "I", "Mp", "Ma", "Fa", "Fp"]) # Output in Rocket and input in Dynamics

        self.add_transient('vEarth', der = 'a', desc = "Rocket velocity")
        self.add_transient('r', der = 'vEarth', desc = "Rocket Position")
        self.add_transient('w', der = 'aw', desc = "Rocket Angular velocity")
        self.add_transient('theta', der = 'w', desc = "Rocket Angular Position")

        self.exec_order = ['Rocket', 'Dyn']

        # self.exec_order = ['Atmo', 'Rocket', 'Dyn']
    
    def compute(self):
        # We need v to be an inward in order to be a transient, thus we add a variable vEarth
        self.v.vector = self.vEarth
