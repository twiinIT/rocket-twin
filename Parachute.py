from cosapp.base import System

from Ports import VelPort, AclPort
from DynamicsPar import DynamicsPar
from Aerodynamics.Aerodynamics import Aerodynamics

import numpy as np

class Parachute(System):
    
    def setup(self):
        
        self.add_inward('l0', 1., desc = "Rope rest length", unit = 'm')
        self.add_inward('k', 100., desc = "rope's stiffness", unit = 'N/m')
        self.add_inward('m1', desc = "Mass of parachute + nosecone", unit = 'kg')
        self.add_inward('m2', desc = "Mass of rocket - nosecone", unit = 'kg')
        self.add_inward('ang', desc = "Angular position of the Rocket in the earth referential, needed for the initialisation of the rope direction", unit = '')

        #Rocket children
        self.add_child(DynamicsPar('DynPar'), pulling = ['g', 'v_wind', 'l0', 'm1', 'm2', 'k', 'r_in', 'v_in', 'ang'])