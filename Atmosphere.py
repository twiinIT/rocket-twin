import numpy as np
from cosapp.base import System, Port

class Atmosphere(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('rhosol', 1., desc="Air Density at Sea Level")
        self.add_inward('Psol', 1., desc="Atmospheric Pressure at Sea Level")
        self.add_inward('Hd', 1., desc="Height Scale of Exponential Fall for Density")
        self.add_inward('Hp', 1., desc="Height Scale of Exponential Fall for Pressure")

        #Trajectory inputs
        self.add_inward('z', 1., desc="Rocket Height")
        
        #Atmosphere outputs
        self.add_outward('rho', 1., desc="Air Density")
        self.add_outward('Pa', 1., desc="Atmospheric Pressure")
        
    def compute(self):

        self.rho = self.rhosol*np.exp(-self.z/self.Hd)
        self.Pa = self.Psol*np.exp(-self.z/self.Hp)