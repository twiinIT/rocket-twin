from cosapp.base import System

import numpy as np

class Coefficients(System):
    def setup(self):
        self.add_inward('alpha', 0., desc='angle of attack', unit='') 
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 

        # Rocket's Geometry
        self.add_inward('ln', 0.2, desc="Length of the cone", unit='m')
        self.add_inward('dn', 0.15, desc='Rocket caliber', unit='m')
        self.add_inward('l', 2, desc = "Rocket length", unit = 'm')
        self.add_inward('xf', self.l - 0.2, desc = "Rocket minus fins length", unit = 'm')

        #Fins' Geometry, check the plan for explanation
        self.add_inward('lr', 0.16, unit = 'm')
        self.add_inward('lt', 0.12, unit='m')
        self.add_inward('ls', 0.12, unit = 'm')
        self.add_inward('lw', 0.05, unit = 'm')
        self.add_inward('lm', 0.2, unit = 'm')
        self.add_inward('lts', 2*self.ls + self.dn, unit = 'm')
        self.add_inward('tf', 0.005, desc = 'Thickness', unit='m')
        
        #Coefficients outwards
        self.add_outward('Cd', 0., desc='Drag coefficient', unit='')
        self.add_outward('Cn', 0., desc='Normal coefficient', unit='')
        self.add_outward('Xcp', 0., desc='CPA position from the rocket top', unit='m')
        self.add_outward('S_ref', np.pi*(self.dn/2)**2, desc="Reference Surface", unit="m**2")


    def compute(self):

        if np.linalg.norm(self.v_cpa)>10:
            cna_c = 2
            cna_b = 0
            cna_f = (1 + self.dn/(self.ls + self.dn/2))*4*4*(self.ls/self.dn)**2/(1 + (1 + 2*self.lm/(self.lr + self.lt))**0.5)
            cna = cna_c + cna_b + cna_f

            self.Cn = cna*self.alpha

            self.Xcp = 1/cna*(cna_c*2/3*self.ln + cna_f*(self.xf + self.lm*(self.lr + 2*self.lt)/(3*(self.lr+self.lt)) + 1/6*(self.lr + self.lt - self.lr*self.lt/(self.lr+self.lt))))

            Rec = 5*10**5
            Ref =  Rec #np.linalg.norm(self.v_cpa) * self.l / (15.6*10**(-6))
            Refb = Rec #np.linalg.norm(self.v_cpa) * self.lm / (15.6*10**(-6))

            Bf = Rec * (0.074/Ref**0.2) - 1.328/Ref**0.5
            Bfb = Rec * (0.074/Refb**0.2) - 1.328/Refb**0.5

            cffb = 1.328/Refb**0.5 if Refb < Rec else 0.074/Refb**0.2 - Bfb/Refb
            cff = 1.328/Ref**0.5 if Ref < Rec else 0.074/Ref**0.2 - Bf/Ref

            afe = 1/2 * (self.lr + self.lt)*self.ls
            afb = afe + 0.5*self.dn*self.lr
            cdi = 2*cff*(1+2*self.tf/self.lm)*4*4*(afb - afe)/(np.pi*self.dn**2)
            cdf = 2*cff*(1+2*self.tf/self.lm)*4*4*(afb)/(np.pi*self.dn**2)
            cdfb = (1 + 60/(self.l/self.dn)**3 + 0.0025*self.l/self.dn)*(2.7*self.l/self.dn + 4*self.l/self.dn)*(cffb)
            cdb = 0.029/cdfb**0.5
            cd0 = cdfb + cdb + cdf + cdi
            cdba = 2*0.9*self.alpha**2 + 3.6*0.7*(1.36*self.l - 0.55*self.ln)/(np.pi*self.dn)*self.alpha**3
            rs = self.lts/self.dn
            kfb = 0.8065*rs**2 + 1.1553*rs
            kbf = 0.1935*rs**2 + 0.8174*rs + 1
            cdfa = self.alpha**2*(1.2*afb**4/(np.pi*self.dn**2) + 3.12*(kfb + kbf - 1)*afe**4/(np.pi*self.dn**2))
            self.Cd = cd0 + cdba + cdfa 
