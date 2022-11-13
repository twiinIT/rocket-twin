
from cosapp.base import System


from Atmosphere import Atmosphere
from Dynamics import Dynamics
from Mass import Mass
from Thrust import Thrust
from Aerodynamics import Aerodynamics

class Rocket(System):
    
    def setup(self):
        
        self.add_child(Dynamics('Dyn'), pulling = ["a", "aw", "m"])
        self.add_child(Aerodynamics('Aero'), pulling = ["V", "theta"])
        self.add_child(Thrust('Thrust'), pulling= ["theta"])
        self.add_child(Mass('Mass'), pulling = ["Dm", "m"])
        # self.add_child(Atmosphere('Atm'), pulling = ["rhosol", "Psol", "Hp", "Hd"])

        self.connect(self.Dyn, self.Aero, {'Fa' : 'Fa', 'Ma' : 'Ma'})
        self.connect(self.Dyn, self.Thrust, {'F' : 'F'})
        self.connect(self.Mass, self.Thrust, {'m' : 'm'})
        self.connect(self.Dyn, self.Mass, {'I' : 'I'})
        # self.connect(self.Atmosphere, self.Aerodynamics, {'rho' : 'rho'})


        self.add_transient('V', der = 'a', desc = "Rocket Velocity")
        self.add_transient('r', der = 'V', desc = "Rocket Position")
        self.add_transient('w', der = 'aw', desc = "Rocket Angular Velocity")
        self.add_transient('theta', der = 'w', desc = "Rocket Angular Position")

        self.exec_order = ['Mass', 'Aero', 'Thrust', 'Dyn']
        # self.exec_order = ['Mass', 'Grav', 'Atmo', 'Aero', 'Thrust', 'Dyn']
    