from cosapp.base import System
import numpy as np

class FinsAero(System):
    
    def setup(self):
        
        #Fins known parameters
        self.add_inward('n', 4., desc="Number of fins", unit='')
        self.add_inward('s', 0.1, desc="Span of one fin", unit='m')
        self.add_inward('Cr', 0.1, desc="See image", unit='m')
        self.add_inward('Ct', 0.1, desc="See image", unit='m')
        self.add_inward('Xt', 0.1, desc="See image", unit='m')
        self.add_inward('tf', 0.001, desc="Fin thickness", unit='m')
        self.add_inward('R_fins', 1., desc="Tube radius at fins' position", unit='m')
        
        #Rocket velocity
        self.add_inward('v', np.zeros(3), desc="Rocket velocity relative to air", unit='m/s')
        
        #Fins aerodynamical values/properties
        self.add_inward('coefs', np.array([1., 1., 1., 1., 0.948, 0.913, 0.854, 0.810, 0.750]), desc="Correction coefficients", unit='')
        self.add_inward('vsound', 340.29, desc="Sound velocity", unit='m/s')
        
        #Fins aerodynamical outputs
        self.add_outward('Cna_1', 2., desc="1 fin normal force coefficient slope", unit='')
        self.add_outward('Cna_fins', 2., desc="Fins normal force coefficient slope", unit='')
        self.add_outward('Cd_fins', 1., desc="Fins drag coefficient", unit='')
        self.add_outward('Xcp_fins', 1., desc="Fins center of pressure", unit='m')
        self.add_outward('Ar_fins', 1., desc="Fins Area of drag effect", unit='m**2')
        self.add_outward('Aw_fins', 1., desc="Fins wetted area", unit='m**2')
        self.add_outward('c_bar', 1., desc="Fins mean aerodynamic chord length", unit='m')
        self.add_outward('y_mac', 1., desc="Position of mean aerodynamic chord length", unit='m')
        self.add_outward('RGC', 1., desc="Roll geometrical constant", unit='')
        self.add_outward('RDIF', 1., desc="Roll damping interference factor", unit='')
        self.add_outward('RFIF', 1., desc="Roll forcing interference factor", unit='')
        
    def compute(self):
        
        ## Source: https://openrocket.info/documentation.html (download first pdf)
        
        #Fins frontal surface (reference area)
        self.Ar_fins = self.n * self.s * self.tf
        
        #Fins lateral surface (wetted area)
        self.Aw_fins = self.n*(self.Ct + self.Cr)*self.s/2
        
        #Fins extended surface
        Af = self.Aw_fins + self.Cr*self.R_fins
        
        #Fins gamma c angle (see image)
        gc = np.atan2(self.Xt + 0.5*(self.Ct - self.Cr),self.s)
        
        #Mach number
        M = np.linalg.norm(self.v)/self.vsound
        
        #Mean aerodynamic chord length
        self.c_bar = (2/3)*(self.Cr + self.Ct + self.Cr*self.Ct/(self.Cr + self.Ct))
        
        #Position of mean aerodynamic chord length
        self.y_mac = (self.s / 3) * (self.Cr + 2 * self.Ct) / (self.Cr + self.Ct)
        
        #Correction coefficients
        if self.n <= 8:
            coef = self.coefs[self.n - 1]
        else:
            coef = self.coefs[8]
            
        #Normal force coefficient slope for one fin
        self.Cna_1 = (self.s/self.R_fins)**2 / (1 + np.sqrt(1 + (self.s**2/(np.cos(gc)*self.Aw_fins))))
        
        #Normal force coefficient slope
        self.Cna_fins = coef * self.n * (1 + self.R_fins/(self.s + self.R_fins)) * self.Cna_1
        
        #Fins center of pressure
        self.Xcp_fins = (self.s*(self.Cr + 2*self.Ct)/(3*np.cos(gc)) + (self.Cr**2 + self.Ct**2 + self.Cr*self.Ct)/6)/(self.Cr + self.Ct)
        
        #Drag coefficient due to drag on fins' base
        Cd_base = 0.12 + 0.13*M**2
        
        #Drag coefficient due to pressure drag on fins
        Cd_fin_pressure = ((1 - M**2)**(-0.417) - 1)*np.cos(gc)**2
        
        #Total drag coefficient
        self.Cd_fins = Cd_base + Cd_fin_pressure
        
        #### Rolling Coefficients ####
        
        #Adimensional parameters
        lbd = self.Ct / self.Cr
        tau = (self.s + self.R_fins) / self.R_fins
        
        #Roll geometrical constant
        self.RGC = (
            (self.Cr + 3 * self.Ct) * self.s**3
            + 4 * (self.Cr + 2 * self.Ct) * self.R_fins * self.s**2
            + 6 * (self.Cr + self.Ct) * self.s * self.R_fins**2
        ) / 12
        
        
        #Roll damping interference factor
        self.RDIF = 1 + (
            ((tau - lbd) / (tau)) - ((1 - lbd) / (tau - 1)) * np.log(tau)
        ) / (
            ((tau + 1) * (tau - lbd)) / (2) - ((1 - lbd) * (tau**3 - 1)) / (3 * (tau - 1))
        )
        
        
        #Roll forcing interference factor
        self.RFIF = (1 / np.pi**2) * (
            (np.pi**2 / 4) * ((tau + 1) ** 2 / tau**2)
            + ((np.pi * (tau**2 + 1) ** 2) / (tau**2 * (tau - 1) ** 2))
            * np.arcsin((tau**2 - 1) / (tau**2 + 1))
            - (2 * np.pi * (tau + 1)) / (tau * (tau - 1))
            + ((tau**2 + 1) ** 2)
            / (tau**2 * (tau - 1) ** 2)
            * (np.arcsin((tau**2 - 1) / (tau**2 + 1))) ** 2
            - (4 * (tau + 1))
            / (tau * (tau - 1))
            * np.arcsin((tau**2 - 1) / (tau**2 + 1))
            + (8 / (tau - 1) ** 2) * np.log((tau**2 + 1) / (2 * tau))
        )