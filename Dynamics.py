from cosapp.base import System

from Ports import VelPort, AclPort

import numpy as np

###DYNAMICS
class Dynamics(System):
    def setup(self):
    
        #System orientation
        self.add_inward('Dyn_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Geometry
        self.add_inward('l', desc = "Rocket length", unit = 'm')
        self.add_inward('I', desc = "Matrix of inertia")
        self.add_inward('m', desc = "mass", unit = 'kg')
        
        #Kinematics inputs
        self.add_input(VelPort, 'v_in')
        self.add_inward('av_in', np.zeros(3), desc = "Rocket Angular Velocity", unit = '1/s')
        
        #AeroForces inputs
        self.add_inward('F', np.zeros(3), desc = "Aerodynamic Force", unit = 'N')
        self.add_inward('Ma', np.zeros(3), desc = "Aerodynamic Moment", unit = 'N*m')
        
        #Thrust input
        self.add_inward('Fp', np.zeros(3), desc="Thrust Force", unit = 'N')
        self.add_inward('Mp', np.zeros(3), desc="Thrust Moment", unit = 'N*m')

        #Gravity inputs
        self.add_input(AclPort, 'g')
        
        #Dynamics outputs
        self.add_outward('a', np.zeros(3), desc = "Rocket Acceleration", unit = 'm/s**2')
        self.add_outward('aa', np.zeros(3), desc = "Rocket Angular Acceleration", unit = '1/s**2')
        
    def compute(self):

        I = self.I
        g = self.g.val

        v = self.v_in.val
        av = self.av_in
        
        #Acceleration
        self.a[0] = (self.F[0] + self.Fp[0])/self.m + g[0] + av[2]*v[1] - av[1]*v[2]
        self.a[1] = (self.F[1] + self.Fp[1])/self.m + g[1] + av[0]*v[2] - av[2]*v[0]
        self.a[2] = (self.F[2] + self.Fp[2])/self.m + g[2] + av[1]*v[0] - av[0]*v[1]
        
        #Angular acceleration (no momentum associated to thrust)
        self.aa[0] = (self.Mp[0] + self.Ma[0] + (I[1] - I[2])*av[1]*av[2])/I[0] 
        self.aa[1] = (self.Mp[1] + self.Ma[1] + (I[2] - I[0])*av[2]*av[0])/I[1]
        self.aa[2] = (self.Mp[2] + self.Ma[2] + (I[0] - I[1])*av[0]*av[1])/I[2]
