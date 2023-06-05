from cosapp.base import System
from Earth import Earth

class Cal_coef(Earth):

    def setup(self):

        super().setup()
        self.add_inward('eps_cal', 1., desc = "Calibration Coefficient", unit = '')