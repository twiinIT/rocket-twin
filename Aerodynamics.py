import numpy as np
from cosapp.base import System
from Utility import aeroCoefs

class Aerodynamics(System):
    
    def setup(self):
        
        #Rocket inputs
        self.add_inward('Sref', 1.767e-2, desc = "Aerodynamic Surface of Reference")
        # self.add_inward('Cd', 1., desc = "Drag Coefficient")
        # self.add_inward('Cl', 1., desc = "Lift Coefficient")
        # self.add_inward('gf', 1., desc = "GF Distance")

        #Trajectory inputs
        self.add_inward('V', np.ones(2), desc = "Rocket velocity")
        self.add_inward('theta', 0., desc = "Rocket direction")

        #Atmosphere inputs
        self.add_inward('rho', 1.225, desc = "Air density")

        #Aerodynamics outputs
        self.add_outward('Fa', np.zeros(2), desc = "Aerodynamic Force")
        self.add_outward('Ma', 0., desc = "Aerodynamic Moment")
        
    def compute(self):
        arctan = np.arctan(self.V[1] / self.V[0]) if self.V[0] > 1e-5 else np.pi/2
        incidence = abs(arctan - self.theta)

        Cx, Cn, Z_CPA = aeroCoefs(incidence)

        self.Fa = 0.5*self.rho*np.linalg.norm(self.V)**2*self.Sref*np.array([Cx, Cn*np.sign(incidence)]) # Selon l'axe de la fusée

        G = 300
        self.Ma = self.Fa[1]*(G - Z_CPA)/1000 # Bras de levier entre Le centre de masse et le centre de poussée aérodynamique

        cos = np.cos(self.theta) if abs(self.theta - np.pi/2) > 1e-5 else 0
        
        #print(cos, self.Fa, Cn, incidence, self.theta, self.V)

        self.Fa = np.array([-self.Fa[0]*cos - self.Fa[1]*np.sin(self.theta),
                            -self.Fa[0]*np.sin(self.theta) + self.Fa[1]*cos]) # Dans le repère cartésien