from cosapp.base import System

from Ports import VelPort, AclPort

import numpy as np

class DynamicsPar(System):
    def setup(self):

        #System orientation
        self.add_inward('DynPar_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        self.add_inward('l0', 1., desc = "Rope rest length", unit = 'm')
        self.add_inward('k', 100., desc = "rope's stiffness", unit='N/m')
        self.add_inward('m1', 1., desc = "Mass of parachute + nosecone", unit = 'kg')
        self.add_inward('m2', 2., desc = "Mass of rocket - nosecone", unit = 'kg')
        self.add_inward('S_ref', .29, desc = "Reference surface of parachute", unit = 'm**2')
        self.add_inward('Cd', 1., desc = "Drag coefficient of parachute", unit = '')
        self.add_inward('r_in', np.zeros(3), desc = "Rocket Position", unit = 'm')
        self.add_inward('temp', np.zeros(3), desc = "Temporary velcity", unit = 'm/s')
        self.add_inward('ang', np.zeros(3), desc = "Rocket angular position", unit = 'm')
        self.add_inward('rho', 1., desc = "Air Density at Rocket's Height", unit = 'kg/m**3')
        self.add_inward('ParaDep', False, desc = "Parachute Deployed", unit = '')
        
        self.add_input(AclPort, 'g')
        self.add_input(VelPort, 'v_wind')
        self.add_input(VelPort, 'v_in')


        #Dynamics outputs
        self.add_outward('a1', np.zeros(3), desc = "Parachute + nosecone Acceleration", unit = 'm/s**2')
        self.add_outward('a2', np.zeros(3), desc = "Rocket - nosecone Acceleration", unit = 'm/s**2')
        self.add_outward('r2_out', np.zeros(3), desc = "Lower String Position", unit = 'm')

        #Transients
        self.add_transient('v1', der='a1')
        self.add_transient('v2', der='a2')
        self.add_transient('r1', der='v1') #correspond au parachute auquel est attaché le nosecone (extrémité haute de la corde)
        self.add_transient('r2', der='v2') #correspond au haut du tube de la fusée (extrémité basse de la corde)

        
    def compute(self):
        if not self.ParaDep:
            return

        Drag = -.5 * self.rho * self.S_ref * self.Cd * np.linalg.norm(self.v1) * (self.v1-self.v_wind.val) 
        d = -self.r2 + self.r1
        self.a1 = -(self.k / self.m1) * (d-self.l0*d/np.linalg.norm(d)) + np.array([0.,0.,-9.8]) + Drag/self.m1
        self.a2 = -(self.k / self.m2) * (-d+self.l0*d/np.linalg.norm(d)) + np.array([0.,0.,-9.8])

        self.r2_out = self.r2