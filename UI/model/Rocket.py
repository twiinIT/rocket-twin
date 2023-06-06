import numpy as np
from Aerodynamics.Aerodynamics import Aerodynamics
from cosapp.base import System
from Dynamics import Dynamics
from Kinematics import Kinematics
from Mass import Mass
from Ports import AclPort, VelPort
from Thrust import Thrust


class Rocket(System):
    def setup(self):
        # System orientation
        self.add_inward("Rocket_ang", np.zeros(3), desc="Earth Euler Angles", unit="")

        # Gravity input
        self.add_input(AclPort, "g")
        self.add_input(VelPort, "v_wind")

        # Rocket parameters
        self.add_inward("l", 0.834664, desc="Rocket length", unit="m")

        # Parachute deployment
        self.add_inward("ParaDep", False, desc="Parachute Deployed", unit="")

        # Rocket children
        self.add_child(Kinematics("Kin"), pulling=["v_out", "Kin_ang", "ParaDep"])
        self.add_child(Thrust("Thrust"), pulling=["l"])
        self.add_child(Dynamics("Dyn"), pulling=["g", "l", "ParaDep"])
        self.add_child(Aerodynamics("Aero"), pulling=["l", "rho", "v_wind", "ParaDep"])
        self.add_child(Mass("Mass"))

        # Child-Child connections
        self.connect(
            self.Kin,
            self.Dyn,
            {"Kin_ang": "Dyn_ang", "v_out": "v_in", "a": "a", "aa": "aa"},
        )
        self.connect(
            self.Kin,
            self.Aero,
            {"Kin_ang": "Aero_ang", "v_cpa": "v_cpa", "av_out": "av"},
        )
        self.connect(self.Dyn, self.Aero, ["F", "Ma"])
        self.connect(self.Thrust, self.Dyn, ["Fp", "Mp"])
        self.connect(self.Mass, self.Dyn, {"m_out": "m", "I": "I"})
        self.connect(self.Mass, self.Aero, {"m_out": "m", "CG_out": "CG"})
        self.connect(self.Mass, self.Thrust, {"CG_out": "CG"})

        # Execution order
        self.exec_order = ["Mass", "Thrust", "Aero", "Dyn", "Kin"]
