from cosapp.base import System
from nose_geom import NoseGeom
from nose_aero import NoseAero

class Nose(System):

    def setup(self):
        
        #Nose known parameters
        self.add_inward('R_nose', 1., desc="Nose radius", unit='m')
        self.add_inward('L_nose', 1., desc="Nose length", unit='m')
        self.add_inward('rho', 300., desc="Nose Density", unit='kg/m**3')
        
        #Nose children
        self.add_child(NoseGeom('geom'), pulling=['R_nose', 'L_nose', 'rho', 'Xcg_nose', 'm_nose', 'I_nose'])
        self.add_child(NoseAero('aero'), pulling=['R_nose', 'L_nose', 'Cna_nose', 'Cd_nose', 'Xcp_nose', 'Ar_nose', 'Aw_nose'])