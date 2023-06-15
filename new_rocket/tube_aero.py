from cosapp.base import System
import numpy as np

class TubeAero(System):
    
    def setup(self):
        
        #Tube known parameters
        self.add_inward('R_tube', 1., desc="Tube radius", unit='m')
        self.add_inward('L_tube', 1., desc="Tube length", unit='m')
        
        #Tube aerodynamical outputs
        self.add_outward('Cna_tube', 0., desc="Tube normal force coefficient slope", unit='')
        self.add_outward('Cd_tube', 0., desc="Tube drag coefficient", unit='')
        self.add_outward('Xcp_tube', 1., desc="Tube center of pressure", unit='m')
        self.add_outward('Aw_tube', 1., desc="Tube wetted surface", unit='m**2')
        
    def compute(self):
        
        #Tube center of pressure
        self.Xcp_tube = self.L_tube/2
        
        #Tube lateral surface (wetted surface)
        self.Aw_tube = 2*np.pi*self.R_tube*self.L_tube