from cosapp.base import System

import numpy as np

class AeroForces(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")

        #Density inputs
        self.add_inward('rho', 1., desc = "Air Density", unit = 'kg/m**3')
        
        #Geometry inputs
        self.add_inward('S_ref', 1., desc = "Rocket Surface of Reference", unit = 'm**2')
        
        #RelativeSpeed inputs
        self.add_inward('V_rel', np.zeros(3), desc = "Relative Speed", unit = 'm/s')
        
        #Coefficients inputs
        self.add_inward('C', np.zeros(3), desc = "Aerodynamics Coefficients", unit = '')
        
        #CenterOfPressure inputs
        self.add_inward('gf', np.zeros(3), desc = "Rocket Center of Pressure", unit = 'm')
        
        #CenterOfGravity inputs
        self.add_inward('gc', np.zeros(3), desc = "Rocket Center of Mass", unit = 'm')
        
        #AeroForces outputs
        self.add_outward('Fa', np.zeros(3), desc = "Aerodynamics Forces", unit = 'N')
        self.add_outward('Ma', np.zeros(3), desc = "Aerodynamics Moments", unit = 'N*m')
        
    def compute(self):
        
        dl = self.gf - self.gc
        
        self.Fa[0] = -0.5*self.rho*self.S_ref*self.V_rel[0]**2*self.C[0]
        self.Fa[1] =  0.5*self.rho*self.S_ref*self.V_rel[0]**2*self.C[1]
        self.Fa[2] = -0.5*self.rho*self.S_ref*self.V_rel[0]**2*self.C[2]
        
        self.Ma[0] = 0.5*self.rho*self.S_ref*self.V_rel[0]**2*self.C[0]*dl[0]
        self.Ma[1] = 0.5*self.rho*self.S_ref*self.V_rel[0]**2*self.C[2]*dl[2]
        self.Ma[2] = 0.5*self.rho*self.S_ref*self.V_rel[0]**2*self.C[1]*dl[1]