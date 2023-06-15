from cosapp.base import System
import numpy as np

class Coefficients(System):
    
    def setup(self):
        
        #Fins parameters
        self.add_inward('Cd_fins', 1., desc="Fins drag coefficient", unit='')
        self.add_inward('Cna_fins', 1., desc="Fins normal force coefficient slope", unit='')
        self.add_inward('Ar_fins', 1., desc="Fins reference area", unit='m**2')
        self.add_inward('Aw_fins', 1., desc="Fins wetted area", unit='m**2')
        self.add_inward('tf', 0.001, desc="Fins thickness", unit='m')
        self.add_inward('c_bar', 1., desc="Mean aerodynamic chord length", unit='m')
        
        #Nose parameters
        self.add_inward('Cd_nose', 1., desc="Fins drag coefficient", unit='')
        self.add_inward('Cna_nose', 1., desc="Fins normal force coefficient slope", unit='')
        self.add_inward('Ar_nose', 1., desc="Nose reference area", unit='m**2')
        self.add_inward('Aw_nose', 1., desc="Nose wetted area", unit='m**2')
        self.add_inward('L_nose', 1., desc="Nose length", unit='m')
        
        #Tube parameters
        self.add_inward('Aw_tube', 1., desc="Tube wetted area", unit='m**2')
        self.add_inward('R_tube', 1., desc="Tube radius", unit='m')
        self.add_inward('L_tube', 1., desc="Tube length", unit='m')
        
        #Rocket parameters
        self.add_inward('Rs', 20*10**(-6), desc="Surface roughness", unit='m')
        self.add_inward('v', np.zeros(3), desc="Rocket velocity relative to air", unit='m/s')
        
        #Environment parameters
        self.add_inward('nu', 1., desc="Kinematic viscosity", unit='m**2/s')
        self.add_inward('vsound', 340.29, desc="Sound velocity", unit='m/s')
        
        #Coefficients values
        self.add_outward('Cd', 1., desc="Rocket drag coefficient", unit='')
        self.add_outward('Cn', 1., desc="Rocket normal force coefficient", unit='')
        
    def compute(self):
        
        #### DRAG COEFFICIENT ####
        
        #Rocket velocity
        v = np.linalg.norm(self.v)
        
        #Angle of attack
        alpha = (np.arccos(self.v[0]/v) if v > 0.1 else 0)
        
        #Mach number
        M = v/self.vsound
        
        #Rocket finesse ratio
        f = 0.5*(self.L_nose + self.L_tube)/self.R_tube
        
        #Skin friction drag coefficient computation
        
        #Reynolds number
        Re = (self.L_nose + self.L_tube) * v / self.nu
        
        #Critical Reynolds number
        Rc = 51 * (self.Rs/(self.L_nose + self.L_tube))**(-1.039)
        
        #Computation of skin friction coefficient
        if Re < 10**4:
            Cf = 1.48 * 10**(-2)
        elif Re > 10**4 and Re < Rc:
            Cf = 1 / (1.5 * np.log(Re) - 5.6)**2
        else:
            Cf = 0.032 * (self.Rs / (self.L_nose + self.L_tube))**0.2
        
        #Correction for compressible flow
        Cf *= (1 - 0.1 * M**2)
        
        #Scaling to correct reference area
        Cf *= ((1 + 0.5/f)*(self.Aw_nose + self.Aw_tube) + (1 + 2*self.tf/self.c_bar)*self.Aw_fins)/(self.Ar_nose + self.Ar_fins)
        
        #Computation of total drag coefficient
        
        self.Cd = (self.Cd_nose * self.Ar_nose + self.Cd_fins*self.Ar_fins)/(self.Ar_nose + self.Ar_fins) + Cf
        
        #Correction for non-zero angle of attack
        
        def f(alpha):
            if alpha <= 17 * np.pi / 180:
                return -22.970602 * alpha**3 + 10.22327 * alpha**2 + 1
            else:
                return (
                    1.25711 * (alpha - 17 * np.pi / 180) ** 3
                    - 2.40250 * (alpha - 17 * np.pi / 180) ** 2
                    + 1.3
                )
            
        self.Cd *= f(np.abs(self.alpha))
        
        #### NORMAL FORCE COEFFICIENT ####
        
        self.Cn = (self.Cna_nose + self.Cna_fins)*alpha