from cosapp.base import System

import numpy as np

from Ports import VelPort

class Coefficients(System):
    def setup(self):

        self.add_inward('Coefs_ang', np.zeros(3), desc="Computing artefact, don't worry")

        #Speed
        self.add_inward('v_cpa', np.zeros(3), desc='CPA velocity', unit='m/s') 
        self.add_inward('av', np.zeros(3), desc = "Rocket Angular Velocity (pqr)", unit = '1/s')

        #Atmosphere
        self.add_inward('rho', 1.292, unit="kg/m**3")
        self.add_inward('nu', 1.5 * 10**-5, unit="m/s**2")

        #Wind
        self.add_input(VelPort, 'v_wind')

        # Rocket's Geometry
        self.add_inward('d', 0.029, desc='Rocket diameter', unit='m')
        self.add_inward('l', -1, desc = "Rocket length", unit = 'm')
        self.add_inward('ln', 0.1, desc="Length of the cone", unit='m')
        self.add_outward('S_ref', np.pi*(self.d/2)**2, desc="Reference Surface", unit="m**2")
        self.add_inward('A0', 0., desc = "Cross section at the top of the body", unit = 'm**2')
        self.add_inward('Al', self.S_ref, desc = "Cross section at the bottom of the body", unit = 'm**2')

        #Fins' Geometry, check the documentation for explanation
        self.add_inward('NFins', 3, desc="Number of fins", unit="")
        self.add_inward('GammaC', 11.3*np.pi/180, desc = 'Fin mid-chord sweep angle', unit="m")
        self.add_inward('s', 0.05, desc="Span of one fin", unit='m')
        self.add_inward('Xt', 0.01, unit = 'm')
        self.add_inward('Cr', 0.06, unit = 'm')
        self.add_inward('Ct', 0.04, unit = 'm')
        self.add_inward('delta', 0.01, desc="Cant angle", unit = '')
        self.add_inward('tf', 0.00456, desc = 'Thickness', unit='m')
        
        #Coefficients outwards
        self.add_outward('Cd', 0.7, desc='Drag coefficient', unit='')
        self.add_outward('N', 0., desc='Normal force')
        self.add_outward('M', 0., desc='Pitch moment')
        self.add_outward('Mroll', 0., desc='Roll moment')
        self.add_outward('Xcp', 0., desc='CPA position from the rocket top', unit='m')

        #Parachute
        self.add_inward_modevar('ParaDep', 0., desc = "Parachute Deployed", unit = '')

    def compute(self):
        if self.ParaDep == 1:
            return
        
        self.v_cpa += self.v_wind.val 

        v_norm = np.linalg.norm(self.v_cpa)

        alpha = np.arccos(self.v_cpa[0]/v_norm) if v_norm>0.1 else 0 #angle d'attaque

        #TODO -v_wind
        M = v_norm / 340.29 # Mach number
        Beta = np.sqrt(abs(M**2-1)) #In our case, we will almost always have a subsonic flight with M<1

        r = self.d/2
        l_t = (self.l - self.ln) # Location of Fin Leading Edge Intersection with body, measured from nose tip
        Yma = self.s/3 * (self.Cr + 2 * self.Ct) / (self.Cr + self.Ct) # Span wise position of the mean aerodynamic chord
        Afin = (self.Cr + self.Ct)/2 * self.s #One sided area
        V = (self.l - self.ln)*self.Al + 1/3*self.ln*np.pi*(self.d/2)**2 # Volume of the body


        Cna_one_fin = (2*np.pi*self.s**2/self.S_ref )/(1 + (1 + (Beta*self.s**2/(Afin*np.cos(self.GammaC)))**2)**0.5)
        # print("Normal coef for a single fin", Cna_one_fin)
        Cna_all_fins = Cna_one_fin * self.NFins/2 # TODO The formula becomes false for NFins>5
        Cna_all_fins = Cna_all_fins * (1 + r/(self.s + r)) # We need to take into account the fin-body interference
        # print("interference factor", (1 + r/(self.s + r)))
        # print("Normal coef for 4 fins", Cna_all_fins)
        Cna_body = 2/self.S_ref*(self.Al - self.A0) #*np.sin(self.alpha)/self.alpha
        # print("Cna body", Cna_body) 

        Cma_body = 2/(self.S_ref*self.d)*(self.l*self.Al - V) #*np.sin(self.alpha)/self.alpha
        # print("Cma body", Cma_body) 

        Cna = Cna_all_fins + Cna_body
        Cma = Cma_body

        Cn = Cna*alpha
        Cm = Cma*alpha #Check the formula, it is calculated at the top nose here and should be calculated at the CG

        Xbody = (self.l*self.Al - V)/(self.Al - self.A0)
        # print("CP Body", Xbody)

        Xfins = l_t + self.Xt/3*(self.Cr+2*self.Ct)/(self.Cr+self.Ct) + 1/6*(self.Cr**2 + self.Ct**2 +self.Cr*self.Ct)/(self.Cr+self.Ct)
        # print(Xfins - l_t)
        self.Xcp = (Xbody*Cna_body + Xfins*Cna_all_fins)/Cna

        # print(f'{self.Xcp=}')
        # print(f'{Cna=}')
        # print(f'{Cn=}')
        # print(f'{Cma=}')
        # print(f'{Cm=}')

        self.N = 0.5*Cn*self.rho*v_norm**2*self.S_ref
        self.M = 0.5*Cm*self.rho*v_norm**2*self.S_ref*self.d
          
        # Parameters for Roll Moment.
        # Documented at: https://github.com/RocketPy-Team/RocketPy/blob/master/docs/technical/aerodynamics/Roll_Equations.pdf
        λ = self.Ct / self.Cr
        tau = (self.s + r) / r

        rollGeometricalConstant = (
            (self.Cr + 3 * self.Ct) * self.s**3
            + 4 * (self.Cr + 2 * self.Ct) * r * self.s**2
            + 6 * (self.Cr + self.Ct) * self.s * r**2
        ) / 12
        rollDampingInterferenceFactor = 1 + (
            ((tau - λ) / (tau)) - ((1 - λ) / (tau - 1)) * np.log(tau)
        ) / (
            ((tau + 1) * (tau - λ)) / (2) - ((1 - λ) * (tau**3 - 1)) / (3 * (tau - 1))
        )
        rollForcingInterferenceFactor = (1 / np.pi**2) * (
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

        Clfd = rollForcingInterferenceFactor * self.N * (r + Yma) * Cna_one_fin / self.d

        Cldw = 2*rollDampingInterferenceFactor * self.N * Cna_one_fin * np.cos(self.delta) * rollGeometricalConstant/ (self.S_ref * self.d**2)

        # print(f'{Clfd=}')
        # print(f'{Cldw=}')

        # print(f'{rollDampingInterferenceFactor=}')
        # print(f'{rollForcingInterferenceFactor=}')

        Mlf = 1 / 2 * self.rho * v_norm**2* self.S_ref * self.d * Clfd * self.delta

        # print(f'{self.av[0]=}')
        Mld = 1 / 2 * self.rho * v_norm * self.S_ref * self.d**2 * Cldw * self.av[0] / 2
        self.Mroll = Mlf - Mld
        # print(f'{self.Mroll=}')


        ############ Drag coefficient ############

        Afin = (self.Cr+self.Ct)/2*self.s #One sided area

        A_ref = (r)**2 * np.pi
        A_wet_body = np.pi * r * (self.ln**2 + r**2)**0.5
        A_wet_fins = 2 * self.NFins * Afin 
        A_wet = A_wet_fins + A_wet_body
        t = .0005 #ailerons de 5mm d'épaisseur
        f_B = self.l/self.d
        c_bar = 2/3*(self.Cr + self.Ct - self.Cr*self.Ct/(self.Cr + self.Ct)) #Mean aerodynamical chord 


        ###Reynolds
        R = self.l * v_norm / self.nu


        ##Skin friction drag
        R_s = 20 #dépend de la surface
        R_crit = 51 * (R_s/self.l)**(-1.039)

        if R<10**4:
            C_f = 1.48*10**-2
        elif R>10**4 and R<R_crit:
            C_f = 1/(1.5*np.log(R) - 5.6)**2
        else:
            C_f = .032*(R_s/self.l)**.2


        C_f_c = C_f * (1-.1*M**2)

        C_D_friction = C_f_c * ((1+1/(2*f_B))*A_wet_body + (1+2*t/c_bar)*A_wet_fins)/A_ref

        # print("Cd friction", C_D_friction)

        #Body pressure drag

        phi = np.arctan(self.d/(2*self.ln))
        C_D_nose_pressure = .8 * np.sin(phi)**2

        C_D_base_pressure = .12 + .13*M**2

        C_D_fin_pressure = (1 - M**2)**(-0.417) - 1

        C_D_fin_pressure *= np.cos(self.GammaC)**2

        C_D_fins = C_D_fin_pressure + C_D_base_pressure

        A_nose = A_ref
        A_fin = self.NFins * t * self.s

        C_D_0 = 1/A_ref * (A_nose * C_D_nose_pressure + A_fin * C_D_fins) + C_D_friction

        def f(alpha):
            if alpha<= 17*np.pi/180:
                return -22.970602*alpha**3 + 10.22327*alpha**2 + 1
            else:
                return 1.25711*(alpha - 17*np.pi/180)**3 -2.40250*(alpha - 17*np.pi/180)**2 + 1.3


        self.Cd = f(abs(alpha)) * C_D_0
        # print("Cd", self.Cd)