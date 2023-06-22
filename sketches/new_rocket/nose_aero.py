from cosapp.base import System
import numpy as np

class NoseAero(System):
    
    def setup(self):
        
        #Nose known parameters
        self.add_inward('R_nose', 1., desc="Nose radius", unit='m')
        self.add_inward('L_nose', 1., desc="Nose length", unit='m')
        
        #Nose aerodynamical outputs
        self.add_outward('Cna_nose', 2., desc="Nose normal force coefficient slope", unit='')
        self.add_outward('Cd_nose', 1., desc="Nose drag coefficient", unit='')
        self.add_outward('Xcp_nose', 1., desc="Nose center of pressure", unit='m')
        self.add_outward('Ar_nose', 1., desc="Nose effective surface", unit='m**2')
        self.add_outward('Aw_nose', 1., desc="Nose wetted surface", unit='m**2')
        
    def compute(self):
        
        #Nose frontal area (reference area)
        self.Ar_nose = np.pi * self.R_nose**2
        
        #Nose lateral area (wetted area)
        self.Aw_nose = np.pi * self.R_nose * np.sqrt(self.R_nose**2 + self.L_nose**2)
        
        #Nose center of pressure
        self.Xcp_nose = 2*self.L_nose/3
        
        #Nose drag coefficient
        self.Cd_nose = 0.8*self.R_nose**2/(self.R_nose**2 + self.L_nose**2)