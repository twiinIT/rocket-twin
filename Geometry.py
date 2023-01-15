from cosapp.base import System


from Geom.CenterOfGravity import CenterOfGravity
from Geom.Mass import Mass
from Geom.Dimensions import Dimensions
from Geom.Inertia import Inertia

class Geometry(System):
    
    def setup(self):
        self.add_inward('referential', 'Rocket', desc = "Thrust is in the Rocket's referential")
    
        #Geometry children
        self.add_child(Mass('Mass'), pulling = ['m_out', 'qp'])
        self.add_child(Inertia('Inertia'), pulling = ['I'])
        self.add_child(Dimensions('Dime'), pulling = ['S', 'S_ref'])
        self.add_child(CenterOfGravity('CoG'), pulling = ['gc'])
        
        #Children-children connections
        self.connect(self.Dime, self.CoG, ['l'])
        self.connect(self.Dime, self.Inertia, ['l', 'r_cyl'])
        self.connect(self.Mass, self.Inertia, {'m_out' : 'm_in'})
        
        #Execution order
        self.exec_order = ['Dime', 'Mass', 'Inertia', 'CoG']
    