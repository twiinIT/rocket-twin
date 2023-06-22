from cosapp.base import System
import numpy as np

class FinsGeom(System):
    
    def setup(self):
        
        #Fins known parameters
        self.add_inward('n', 4., desc="Number of fins", unit='')
        self.add_inward('s', 0.1, desc="Span of one fin", unit='m')
        self.add_inward('Cr', 0.1, desc="See image", unit='m')
        self.add_inward('Ct', 0.1, desc="See image", unit='m')
        self.add_inward('Xt', 0.1, desc="See image", unit='m')
        self.add_inward('tf', 0.001, desc="Fin thickness", unit='m')
        self.add_inward('R_fins', 1., desc="Tube radius at fins' position", unit='m')
        self.add_inward('rho', 300., desc="Fin material density", unit = 'kg/m**3')
        
        #Fins geometric outputs
        self.add_outward('Xcg_fins', 1., desc="Center of gravity x-coordinate", unit='m')
        self.add_outward('m_fins', 1., desc="Fins mass", unit='kg')
        self.add_outward('I_fins', np.ones(3), desc="Fins principal inertia moments", unit='kg*m**2')
        
    def compute(self):
        
        #Gamma c (see image)
        gc = np.atan2(self.Xt + 0.5*(self.Ct - self.Cr),self.s)
        
        #Fins mass
        self.m_fins = self.n * self.rho * self.tf * (self.Cr + self.Ct)*self.s/2
        
        #Fins center of gravity
        self.Xcg_fins = self.Cr/2 + self.s * np.tan(gc)/2
        
        #Fins principal inertia moments
        
        Ix = self.n * self.m * (self.s/2 + self.R_fins)**2
        Iy = Ix/2
        
        self.I_fins = np.array([Ix, Iy, Iy])