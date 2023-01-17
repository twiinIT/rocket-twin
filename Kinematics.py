from cosapp.base import System

from Ports import VelPort

import numpy as np

class Kinematics(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
    
        #System orientation
        self.add_outward('Kin_ang', np.zeros(3), desc = "Rocket Euler Angles", unit = '')
        
        #Dynamics inputs
        self.add_inward('a', np.zeros(3), desc = "Rocket Acceleration", unit = 'm/s**2')
        self.add_inward('aa', np.zeros(3), desc = "Rocket Angular Acceleration", unit = '1/s**2')
        self.add_outward('av2', np.zeros(3), desc = "Rocket Angular Velocity", unit = '1/s')
        
        #Kinematics transients
        self.add_transient('v', der = 'a', desc = "Rocket Velocity")
        self.add_transient('av', der = 'aa', desc = "Rocket Angular Velocity (pqr)")
        self.add_transient('ar', der = 'av2', desc = "Rocket Angular Position")
        self.add_transient('artest', der = 'av')
        
        #Kinematics outputs
        self.add_output(VelPort, 'v_out')
        self.add_outward('av_out', np.zeros(3), desc = "Rocket Angular Velocity (pqr)", unit = '1/s')
        
    def compute(self):

        self.av2[0] = self.av[0] + np.tan(self.ar[1])*(self.av[2]*np.cos(self.ar[0]) + self.av[1]*np.sin(self.ar[0]))
        self.av2[1] = self.av[1]*np.cos(self.ar[0]) - self.av[2]*np.sin(self.ar[0])
        self.av2[2] = (self.av[2]*np.cos(self.ar[0]) + self.av[1]*np.sin(self.ar[0]))/np.cos(self.ar[1])

        self.v_out.val = self.v
        self.av_out = self.av
        self.Kin_ang = self.ar

