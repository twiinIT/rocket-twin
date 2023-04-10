from cosapp.base import System

from Atmosphere.Density import Density
from Atmosphere.Pressure import Pressure

class Atmosphere(System):
    
    def setup(self):
        
        #Atmosphere children
        self.add_child(Density('Dens'), pulling = ['r_in', 'rho'])
        self.add_child(Pressure('Pres'), pulling = ['r_in', 'P'])
        
        #Execution order
        self.exec_order = ['Dens', 'Pres']