from cosapp.base import System
import numpy as np
from fins_geom import FinsGeom
from fins_aero import FinsAero

class Fins(System):

    def setup(self):

        #Fins known Parameters
        self.add_inward('n', 4., desc="Number of fins", unit='')
        self.add_inward('s', 0.1, desc="Span of one fin", unit='m')
        self.add_inward('Cr', 0.1, desc="See image", unit='m')
        self.add_inward('Ct', 0.1, desc="See image", unit='m')
        self.add_inward('Xt', 0.1, desc="See image", unit='m')
        self.add_inward('tf', 0.001, desc="Fin thickness", unit='m')
        self.add_inward("delta", 0.0, desc="Fin cant angle", unit="")
        self.add_inward('rho', 300., desc="Fin material density", unit = 'kg/m**3')
        self.add_inward('Lf', 1., desc="Distance from fin tip to nose cone", unit='m')
        self.add_inward('R_fins', 1., desc="Tube radius at fins' position", unit='m')
        
        #Rocket velocity
        self.add_inward('v', np.zeros(3), desc="Rocket velocity relative to air", unit='m/s')
        
        #Fins children
        self.add_child(FinsGeom('geom'), pulling=['n', 's', 'Cr', 'Ct', 'Xt', 'tf', 'R_fins', 'rho', 'Xcg_fins', 'm_fins', 'I_fins'])
        self.add_child(FinsAero('aero'), pulling=['n', 's', 'Cr', 'Ct', 'Xt', 'tf', 'R_fins', 'v', 'Cna_1', 'Cna_fins', 'Cd_fins', 'Xcp_fins', 'Ar_fins', 'Aw_fins', 'c_bar', 'y_mac', 'RGC', 'RDIF', 'RFIF'])