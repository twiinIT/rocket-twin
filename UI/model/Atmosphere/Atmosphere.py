from atmosphere.density import Density
from atmosphere.pressure import Pressure
from cosapp.base import System


class Atmosphere(System):
    def setup(self):
        # Atmosphere children
        self.add_child(Density("Dens"), pulling=["r_in", "r2_in", "rho", "ParaDep"])
        self.add_child(Pressure("Pres"), pulling=["r_in", "r2_in", "P", "ParaDep"])

        # Execution order
        self.exec_order = ["Dens", "Pres"]
