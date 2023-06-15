from cosapp.base import System

class CPA(System):
    
    def setup(self):
        
        #Fins parameters
        self.add_inward('Xcp_fins', 1., desc="Fins center of pressure", unit='m')
        self.add_inward('Cna_fins', 1., desc="Fins normal force coefficient slope", unit='')
        self.add_inward('Lf', 1., desc="Distance from fin tip to nose cone", unit='m')
        
        #Nose parameters
        self.add_inward('Xcp_nose', 1., desc="Nose center of pressure", unit='m')
        self.add_inward('Cna_nose', 1., desc="Fins normal force coefficient slope", unit='')
        
        #Rocket center of pressure
        self.add_outward('Xcp', 1., desc="Rocket center of pressure", unit='m')
        
    def compute(self):
        
        self.Xcp = (self.Cna_nose*self.Xcp_nose + self.Cna_fins*(self.Lf +self.Xcp_fins))/(self.Cna_nose + self.Cna_fins)