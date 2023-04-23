from cosapp.base import System
from ReferentialPort import ReferentialPort
from Utility import aeroCoefs
import numpy as np

class Aerodynamics(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Aerodynamics is in the Rocket's referential")

        #Rocket inputsèè
        self.add_inward('Sref', 1.767e-2, desc = "Aerodynamic Surface of Reference")

        #Trajectory inputs
        self.add_input(ReferentialPort, 'v') # desc = "Rocket velocity"

        #Atmosphere inputs
        self.add_inward('rho', 1.225, desc = "Air density")

        #Aerodynamics outputs
        self.add_output(ReferentialPort, 'Fa') # desc = "Aerodynamic Force"
        self.add_outward('Ma', 0., desc = "Aerodynamic Moment")
        
    def compute(self):
        incidence = self.parent.parent.theta - np.arctan2(self.parent.parent.v.vector[1],self.parent.parent.v.vector[0]) # The y axis is the axis of the rocket and the x axis is perpendicular 

        incidence = incidence%(2*np.pi) - np.pi

        Cx, Cn, Z_CPA = aeroCoefs(incidence) 
        
        self.Fa.vector = 0.5*self.rho*np.linalg.norm(self.v.vector)**2*self.Sref*np.array([Cn, Cx]) # Selon l'axe de la fusée

        G = .300
        self.Ma = self.Fa.vector[0]*(G - Z_CPA) # Bras de levier entre Le centre de masse et le centre de poussée aérodynamique
