from cosapp.base import System

from Ports import VelPort

import numpy as np 

from scipy.spatial.transform import Rotation as R

class Trajectory(System):
    
    def setup(self):
    
        #Rocket inputs
        self.add_input(VelPort, 'v')
        self.add_outward('r_out', np.zeros(3), desc = "Rocket Position", unit="m")

        #Trajectory transients
        self.add_transient('r', der = 'v.val', desc = "Rocket Position")

        self.add_inward('ang', np.zeros(3), desc = "Rocket angular position", unit = '')

        # Rope length of the parachute
        self.add_inward('l0', 1., desc = "Rope rest length", unit = 'm')

        #Event
        self.add_event("Apogee", trigger='v.val[2] < 0')
        self.add_event("ParachuteDeployed", trigger = 'time > 9.')
        self.add_inward("apogee_time", np.Infinity, unit = "s")
        self.add_event("FinallyDeployed", trigger = "time > apogee_time + .1 ") # The parachute takes .1 second to deploy itself

        self.add_outward('ParaDep', 0., desc = "Parachute Deployed", unit = '')

    def transition(self):

        if self.Apogee.present and self.ParaDep  == 0:

            print('\n')
            print("___APOGEE___")
            print('\n')
            print("Flight Time at Apogee: ", self.time, 's')
            print('\n')
            print("X Coordinate at Apogee: ", self.r[0], 'm')
            print('\n')
            print("Y Coordinate at Apogee: ", self.r[1], 'm')
            print('\n')
            print("Z Coordinate at Apogee: ", self.r[2], 'm')
            print('\n')

        if self.ParachuteDeployed.present and self.ParaDep == 0:

            print("___PARACHUTE DEPLOYMENT___")
            print('\n')
            self.apogee_time = self.time
            DynPar = self.parent.Para.DynPar
            DynPar.r1 = self.r
            DynPar.r2 = self.r
            DynPar.v1 = self.v.val
            DynPar.v2 = self.v.val
            l0 = [self.l0,0,0]
            rotation = R.from_euler('xyz', self.ang, degrees=False)
            vectEarth = rotation.apply(l0)
            DynPar.r1 = DynPar.r1 + vectEarth
            #print("coordinates (1,2) at apogee", DynPar.r1, DynPar.r2)
            #print("velocity (1,2) at apogee", DynPar.v1, DynPar.v2)
            #print('Apogee time', self.time)

            print("Point 1 X Coordinate at Deployment: ", DynPar.r1[0], 'm')
            print('\n')
            print("Point 1 Y Coordinate at Deployment: ", DynPar.r1[1], 'm')
            print('\n')
            print("Point 1 Z Coordinate at Deployment: ", DynPar.r1[2], 'm')
            print('\n')
            print("Point 2 X Coordinate at Deployment: ", DynPar.r2[0], 'm')
            print('\n')
            print("Point 2 Y Coordinate at Deployment: ", DynPar.r2[1], 'm')
            print('\n')
            print("Point 2 Z Coordinate at Deployment: ", DynPar.r2[2], 'm')
            print('\n')
            print("___PARACHUTE DEPLOYMENT___")
            
        
        if self.FinallyDeployed.present:
            print("Parachute fully deployed !")
            self.ParaDep = 1


    def compute(self):
        self.r_out = self.r
        # print(self.time)
