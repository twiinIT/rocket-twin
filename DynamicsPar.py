from cosapp.base import System

from Ports import VelPort, AclPort

import numpy as np

from scipy.spatial.transform import Rotation as R


class DynamicsPar(System):
    def setup(self):

        #System orientation
        self.add_inward('DynPar_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        self.add_inward('l0', 1., desc = "Rope rest length", unit = 'm')
        self.add_inward('k', 100., desc = "rope's stiffness", unit='N/m')
        self.add_inward('m1', 1., desc = "Mass of parachute + nosecone", unit = 'kg')
        self.add_inward('m2', 2., desc = "Mass of rocket - nosecone", unit = 'kg')
        self.add_inward('S_ref', .1, desc = "Reference surface of parachute", unit = 'm**2')
        self.add_inward('Cd', 1.75, desc = "Drag coefficient of parachute", unit = '')
        self.add_inward('r_in', np.zeros(3), desc = "Rocket Position", unit = 'm')
        self.add_inward('temp', np.zeros(3), desc = "Temporary velcity", unit = 'm/s')
        self.add_inward('ang', np.zeros(3), desc = "Rocket angular position", unit = 'm')
        self.add_inward('Dep', 0., desc = "Parachute Deployed", unit = '')
        
        self.add_input(AclPort, 'g')
        self.add_input(VelPort, 'v_wind')
        self.add_input(VelPort, 'v_in')


        #Dynamics outputs
        self.add_outward('a1', np.zeros(3), desc = "Parachute + nosecone Acceleration", unit = 'm/s**2')
        self.add_outward('a2', np.zeros(3), desc = "Rocket - nosecone Acceleration", unit = 'm/s**2')

        #Transients
        self.add_transient('v1', der='a1')
        self.add_transient('v2', der='a2')
        self.add_transient('r1', der='v1') #correspond au parachute auquel est attaché le nosecone (extrémité haute de la corde)
        self.add_transient('r2', der='v2') #correspond au haut du tube de la fusée (extrémité basse de la corde)

        #Event
        self.add_event("ParachuteDeployed", trigger='v_in.val[2] < 0')
        self.add_inward("apogee_time", np.Infinity, unit = "s")
        self.add_event("FinallyDeployed", trigger = "time > apogee_time + 1 ") # The parachute takes one second to deploy itself

    def transition(self):

        if self.ParachuteDeployed.present and self.Dep == 0:

            print("___PARACHUTE DEPLOYMENT___")
            self.apogee_time = self.time
            self.r1 = self.r_in
            self.r2 = self.r_in
            self.v1 = self.v_in.val
            self.v2 = self.v_in.val
            l0 = [self.l0,0,0]
            rotation = R.from_euler('xyz', self.ang, degrees=False)
            vectEarth = rotation.apply(l0)
            self.r1 = self.r1 + vectEarth
            print("coordinates (1,2) at apogee", self.r1, self.r2)
            print("velocity (1,2) at apogee", self.v1, self.v2)
            print("___PARACHUTE DEPLOYMENT___")
            
        
        if self.FinallyDeployed.present and self.Dep == 0:
            print("Parachute fully deployed !")
            self.Dep = 1


        
    def compute(self):

        if self.Dep == 1:
            Drag = -.5 * self.S_ref * self.Cd * np.linalg.norm(self.v1) * (self.v1-self.v_wind.val) 
            d = -self.r2 + self.r1
            self.a1 = -(self.k / self.m1) * (d-self.l0*d/np.linalg.norm(d)) + np.array([0.,0.,-9.8]) + Drag/self.m1
            self.a2 = -(self.k / self.m2) * (-d+self.l0*d/np.linalg.norm(d)) + np.array([0.,0.,-9.8])