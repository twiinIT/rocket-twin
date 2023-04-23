import numpy as np
from cosapp.base import System

class Atmosphere(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('rhosol', desc="Air Density at Sea Level")
        self.add_inward('Psol', desc="Atmospheric Pressure at Sea Level")
        self.add_inward('Hd', desc="Height Scale of Exponential Fall for Density")
        self.add_inward('Hp', desc="Height Scale of Exponential Fall for Pressure")

        #Trajectory inputs
        self.add_inward('z', desc="Rocket Height")
        
        #Atmosphere outputs
        self.add_outward('rho', desc="Air Density")
        self.add_outward('Pa', desc="Atmospheric Pressure")
        
    def compute(self):

        self.rho = self.rhosol*np.exp(-self.z/self.Hd)
        self.Pa = self.Psol*np.exp(-self.z/self.Hp)