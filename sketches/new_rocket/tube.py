from cosapp.base import System
from tube_geom import TubeGeom
from tube_aero import TubeAero

class Tube(System):

    def setup(self):
        
        #Tube known parameters
        self.add_inward('R_tube', 1., desc="Tube radius", unit='m')
        self.add_inward('L_tube', 1., desc="Tube length", unit='m')
        self.add_inward('rho', 300., desc="Tube material density", unit='kg/m**3')
        
        #Tube children
        self.add_child(TubeGeom('geom'), pulling=['rho', 'R_tube', 'L_tube', 'Xcg_tube', 'm_tube', 'I_tube'])
        self.add_child(TubeAero('aero'), pulling=['R_tube', 'L_tube', 'Cna_tube', 'Cd_tube', 'Xcp_tube', 'Aw_tube'])