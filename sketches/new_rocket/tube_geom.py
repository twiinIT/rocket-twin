from cosapp.base import System
import numpy as np

class TubeGeom(System):
    
    def setup(self):
        
        #Tube known parameters
        self.add_inward('R_tube', 1., desc="Tube radius", unit='m')
        self.add_inward('L_tube', 1., desc="Tube length", unit='m')
        self.add_inward('rho', 300., desc="Tube material density", unit='kg/m**3')
        
        #Tube geometric outputs
        self.add_outward('Xcg_tube', 1., desc="Center of gravity x-coordinate", unit='m')
        self.add_outward('m_tube', 1., desc="Tube mass", unit='kg')
        self.add_outward('I_tube', np.ones(3), desc="Tube principal inertia moments", unit='kg*m**2')
        
    def compute(self):
        
        #Tube center of gravity
        self.Xcg_tube = self.L_tube/2
        
        #Tube mass
        self.m_tube = self.rho * self.L_tube * np.pi * self.R_tube**2
        
        #Tube inertia moments
        Iy = self.m_tube * self.R_tube**2/4 + self.m_tube * self.L_tube**2/12
        Ix = self.m_tube * self.R_tube**2/2
        
        self.I_tube = np.array([Ix, Iy, Iy])