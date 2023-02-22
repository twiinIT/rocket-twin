from cosapp.base import System

from Atmosphere.Density import Density
from Atmosphere.Pressure import Pressure
from Atmosphere.Wind import Wind

class Atmosphere(System):
    
    def setup(self):
        
        #Atmosphere children
        self.add_child(Density('Dens'), pulling = ['r_in', 'rho'])
        self.add_child(Pressure('Pres'), pulling = ['r_in', 'P'])
        self.add_child(Wind('Wind'), pulling=   ['r_in','v_wind'])
        
        #Execution order
        self.exec_order = ['Dens', 'Wind', 'Pres']