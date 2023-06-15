from cosapp.base import System
import numpy as np

class Moments(System):
    
    def setup(self):
        
        #Fins parameters
        self.add_inward('Cna_1', 2., desc="1 fin normal force coefficient slope", unit='')
        self.add_inward('y_mac', 1., desc="Position of mean aerodynamic chord length", unit='m')
        self.add_inward('RGC', 1., desc="Roll geometrical constant", unit='')
        self.add_inward('RDIF', 1., desc="Roll damping interference factor", unit='')
        self.add_inward('RFIF', 1., desc="Roll forcing interference factor", unit='')
        self.add_inward("delta", 0.0, desc="Fin cant angle", unit="")
        self.add_inward('Ar_fins', 1., desc="Fins reference area", unit='m**2')
        self.add_inward('R_fins', 1., desc="Tube radius at fins' position", unit='m')
        
        #Nose parameters
        self.add_inward('Ar_nose', 1., desc="Nose reference area", unit='m**2')
        
        #Rocket Velocities
        self.add_inward('v', 1., desc="Rocket velocity relative to air", unit='m/s')
        self.add_inward('av', 1., desc="Rocket angular velocity", unit='1/s')
        
        #Atmosphere density
        self.add_inward('rho', 1., desc="Air density at rocket height", unit='kg/m**3')
        
        #Forces
        self.add_inward('Fn', 1., desc="Value of normal aerodynamic force", unit='N')
        self.add_inward('Fa', 1., desc="Total aerodynamic force", unit='N')
        
        #Positions
        self.add_inward('Xcp', 1., desc="Position of center of pressure", unit='m')
        self.add_inward('Xcg', 1., desc="Position of center of gravity", unit='m')
        
        #Total moment
        self.add_outward('Ma', 1., desc="Aerodynamic moment", unit='N*m')
        
    def compute(self):
        
        v = np.linalg.norm(self.v)
        S_ref = self.Ar_fins + self.Ar_nose
        
        #### ROLLING MOMENT ####
        
        #Forcing moment coefficient
        Clfd = self.RFIF*self.Fn*(self.R_fins + self.y_mac)*self.Cna_1/(2*self.R_fins)
        
        #Damping moment coefficient
        Cldw = self.RDIF*self.Fn*self.Cna_1*np.cos(self.delta)*self.RGC/(4*S_ref*self.R_fins**2)
        
        #Forcing moment
        
        Mlf = self.rho * v**2 * S_ref * self.R_fins * Clfd * self.delta
        
        #Damping moment
        
        Mld = self.rho * v * S_ref * self.R_fins**2 * Cldw * self.av[0]
        
        #Total rolling moment
        
        M_roll = Mlf - Mld
        
        
        #### TOTAL MOMENT ####
        
        OM = np.array([self.Xcg - self.Xcp, 0., 0.])
        self.Ma = np.cross(OM, self.Fa)
        self.Ma[0] += M_roll