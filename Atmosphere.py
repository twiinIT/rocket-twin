from cosapp.base import System

import numpy as np

from Atmo.Density import Density
from Atmo.Pressure import Pressure
from Atmo.Wind import Wind

class Atmosphere(System):
    
    def setup(self):
        
        #System orientation
        self.add_inward('Atmo_ang', np.zeros(3), desc = "Earth Euler Angles", unit = '')
        
        #Atmosphere children
        self.add_child(Density('Dens'), pulling = ['r_in', 'rho'])
        self.add_child(Pressure('Pres'), pulling = ['r_in', 'P'])
        self.add_child(Wind('Wind'), pulling = ['V_wind'])
        
        #Execution order
        self.exec_order = ['Dens', 'Pres', 'Wind']
    
    