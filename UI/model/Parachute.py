from cosapp.base import System
from dynamics_par import DynamicsPar


class Parachute(System):
    def setup(self):
        self.add_inward("l0", 0.5, desc="Rope rest length", unit="m")
        self.add_inward("k", 100.0, desc="rope's stiffness", unit="N/m")
        self.add_inward("m1", 1.0, desc="Mass of parachute + nosecone", unit="kg")
        self.add_inward("m2", 2.0, desc="Mass of rocket - nosecone", unit="kg")

        # Rocket children
        self.add_child(
            DynamicsPar("DynPar"),
            pulling=[
                "g",
                "v_wind",
                "m1",
                "m2",
                "l0",
                "k",
                "r_in",
                "v_in",
                "ParaDep",
                "r2_out",
                "rho",
            ],
        )
