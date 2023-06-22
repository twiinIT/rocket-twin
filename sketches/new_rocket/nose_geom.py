from cosapp.base import System
import numpy as np

class NoseGeom(System):
    
    def setup(self):
        
        #Nose known parameters
        self.add_inward('R_nose', 1., desc="Nose radius", unit='m')
        self.add_inward('L_nose', 1., desc="Nose length", unit='m')
        self.add_inward('rho', 300., desc="Nose Density", unit='kg/m**3')
        
        #Nose geometric outputs
        self.add_outward('Xcg_nose', 1., desc="Center of gravity x-coordinate", unit='m')
        self.add_outward('m_nose', 1., desc="Nose mass", unit='kg')
        self.add_outward('I_nose', np.ones(3), desc="Nose principal inertia moments", unit='kg*m**2')
        
    def compute(self):
        
        #Nose volume
        V = self.L_nose*np.pi*self.R_nose**2/3
        
        #Nose mass
        self.m_nose = self.rho*V
        
        #Nose center of gravity
        self.Xcg_nose = 3*self.L_nose/4
        
        #Nose inertia moments
        Ix = (3/10)*self.m_nose*self.R_nose**2
        Iy = (3*self.m_nose/20)*(self.R_nose**2 + self.L_nose**2/4)
        
        self.I_nose = np.array([Ix, Iy, Iy])