from cosapp.base import System
from aeroforces import Aeroforces
from moments import Moments
from coefficients import Coefficients
from cpa import CPA

class RocketAero(System):
    
    def setup(self):
        
        self.add_child(Aeroforces('afor'), pulling=['rho', 'v', 'Ar_fins', 'Ar_nose', 'Fa'])
        self.add_child(Moments('moments'), pulling=['Cna_1', 'y_mac', 'RGC', 'RDIF', 'RFIF', 'delta', 'Ar_fins', 'R_fins', 'Ar_nose', 'v', 'av', 'rho', 'Xcg', 'Ma'])
        self.add_child(Coefficients('coef'), pulling=['Cd_fins', 'Cna_fins', 'Ar_fins', 'Aw_fins', 'tf', 'c_bar', 'Cd_nose', 'Cna_nose', 'Ar_nose', 'Aw_nose', 'L_nose', 'R_tube', 'L_tube', 'Aw_tube', 'v'])
        self.add_child(CPA('cpa'), pulling=['Xcp_fins', 'Cna_fins', 'Lf', 'Xcp_nose', 'Cna_nose'])
        
        self.connect(self.afor, self.coef, ['Cd', 'Cn'])
        self.connect(self.afor, self.moments, ['Fa'])
        self.connect(self.cpa, self.moments, ['Xcp'])