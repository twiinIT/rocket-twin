import numpy as np
from cosapp.base import System


class Mass(System):
    def setup(self):
        self.add_inward(
            "referential", "Rocket", desc="Mass is in the Rocket's referential"
        )

        # Rocket inputs
        self.add_inward("m", 1.639, desc="Rocket's Mass")
        self.add_inward("m0", 1.639, desc="Rocket's Initial Mass")
        self.add_inward("lp", desc="propellant cylinder length", unit="m")
        self.add_inward("Gdm", unit="m")
        self.add_inward("mCG", desc="product", unit="m*kg")
        self.add_inward(
            "I0_geom",
            np.array([10.0, 100.0, 100.0]),
            desc="Rocket's Initial Inertia Moment/mass",
        )

        # Mass outputs
        self.add_outward("I", self.I0_geom * self.m, desc="Rocket's Inertia Moment")
        self.add_inward("Dm", (0.16 - 0.084) / 1, desc="Rocket Mass' Rate of Change")
        self.add_outward("m_out", 0, desc="Rocket's mass", unit="kg")
        self.add_inward(
            "lastEngineTime",
            1.0,
            desc="There is no more engine after this time",
            unit="s",
        )
        self.add_outward("CG_out", 0, desc="Rocket COG", unit="m")

        # Events
        self.add_event("noMoreEngine", trigger="time >= lastEngineTime")

        # Transients
        self.add_transient("m", der="-Dm")
        self.add_transient("Gdm", der="-lp/lastEngineTime")
        self.add_transient("mCG", der="-Dm*Gdm")

    def transition(self):
        if self.noMoreEngine.present:
            self.Dm = 0

    def compute(self):
        self.I = self.I0_geom * self.m / self.m0
        self.m_out = self.m

        self.CG_out = self.mCG / self.m_out
