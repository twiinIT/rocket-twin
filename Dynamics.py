from cosapp.base import System

from Ports import VelPort,AclPort

import numpy as np

class Dynamics(System):
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
    
        #System orientation
        self.add_inward('Dyn_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Kinematics inputs
        self.add_input(VelPort, 'v_in')
        self.add_inward('av_in', np.zeros(3), desc = "Rocket Angular Velocity", unit = '1/s')
        
        #Thrust inputs
        self.add_inward('Fp', np.zeros(3), desc = "Thrust Force", unit = 'N')
        self.add_inward('Mp', np.zeros(3), desc = "Thrust Moment", unit = 'N*m')
        
        #AeroForces inputs
        self.add_inward('Fa', np.zeros(3), desc = "Thrust Force", unit = 'N')
        self.add_inward('Ma', np.zeros(3), desc = "Thrust Moment", unit = 'N*m')
        
        #Geometry inputs
        self.add_inward('m', 100., desc = "Rocket Mass", unit = 'kg')
        self.add_inward('I', np.array([10., 100., 100.]), desc = "Rocket Moments of Inertia", unit = 'kg*m**2')
        
        #Gravity inputs
        self.add_input(AclPort, 'g')
        
        #Dynamics outputs
        self.add_outward('a', np.zeros(3), desc = "Rocket Acceleration", unit = 'm/s**2')
        self.add_outward('aa', np.zeros(3), desc = "Rocket Angular Acceleration", unit = '1/s**2')
        
    def compute(self):
        
        v = self.v_in.val
        av = self.av_in
        
        self.a[0] = (self.Fp[0] + self.Fa[0])/self.m + self.g.val[0] - av[2]*v[1] + av[1]*v[2]*1
        self.a[1] = (self.Fp[1] + self.Fa[1])/self.m + self.g.val[1] - av[0]*v[2] + av[2]*v[0]
        self.a[2] = (self.Fp[2] + self.Fa[2])/self.m + self.g.val[2] - av[1]*v[0] + av[0]*v[1]
        
        self.aa[0] = (self.Mp[0] + self.Ma[0] + (self.I[1] - self.I[2])*av[1]*av[2])/self.I[0]
        self.aa[1] = (self.Mp[1] + self.Ma[1] + (self.I[2] - self.I[0])*av[2]*av[0])/self.I[1]
        self.aa[2] = (self.Mp[2] + self.Ma[2] + (self.I[0] - self.I[1])*av[0]*av[1])/self.I[2]
