from cosapp.base import System
import numpy as np

class Aeroforces(System):
    
    def setup(self):
        
        #Atmosphere parameters
        self.add_inward('rho', 1., desc="Air density at rocket's height", unit='kg/m**3')
        
        #Rocket parameters
        self.add_inward('v', 1., desc="Rocket velocity relative to air", unit='m/s')
        
        #Fins parameters
        self.add_inward('Ar_fins', 1., desc="Fins reference area", unit='m**2')
        
        #Cone parameters
        self.add_inward('Ar_nose', 1., desc="Nose reference area", unit='m**2')
        
        #Coefficient parameters
        self.add_inward('Cd', 1., desc="Rocket drag coefficient", unit='')
        self.add_inward('Cn', 1., desc="Rocket normal force coefficient", unit='')
        
        #Aerodynamic force
        self.add_outward('Fa', np.zeros(3), desc="Aerodynamic force", unit='N')
        
    def compute(self):
        
        v = np.linalg.norm(self.v)
        
        #Normal force
        Fn = 0.5 * self.Cn * self.rho * v**2 * (self.Ar_fins + self.Ar_nose)
        
        #Drag force
        Fd = 0.5 * self.Cd * self.rho * v**2 * (self.Ar_fins + self.Ar_nose)
        
        #Normal force angle
        a = np.arctan2(v[2],v[1])
        
        #Total aerodynamic force
        self.F = np.array([-Fd, -Fn*np.sin(a), -Fn*np.cos(a)])