from cosapp.base import System

from Aerodynamics import Aerodynamics
from Thrust import Thrust
from Mass import Mass 

from ReferentialPort import ReferentialPort

class Rocket(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Rocket is in the Rocket's referential")

        self.add_input(ReferentialPort, 'ref')
        # En dessous inward
        self.add_input(ReferentialPort, 'v')
        self.add_output(ReferentialPort, 'Fa')
        self.add_output(ReferentialPort, 'Fp')

        self.add_child(Aerodynamics('Aero'), pulling = ["v", "Fa", "Ma"])
        self.add_child(Thrust('Thrust'), pulling= ["m", "Fp", "Mp"])
        self.add_child(Mass('Mass'), pulling = ["m", "I"])

        self.exec_order = ['Mass', 'Aero', 'Thrust']
