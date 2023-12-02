import numpy as np
from cosapp.base import System


class Dynamics(System):
    """Dynamics of a physical system.

    Inputs
    ------
    forces [N]: float,
        total force in each component of the system
    weights [kg]: float,
        total weight of each component of the system
    centers[m]: float,
        center of gravity of each component of the system

    Outputs
    ------
    force [N]: float,
        total force
    weight [kg]: float,
        total weight
    a [m/s**2] : float,
        acceleration
    """

    def setup(self, forces=None, weights=None):
        if forces is None:
            forces = []
        if weights is None:
            weights = []

        self.add_property("forces", forces)
        self.add_property("weights", weights)

        # inwards
        self.add_inward("pos", np.array([0., 0., 6400.0e3]), desc="local position", unit="m")
        self.add_inward("g0", -10.0, desc="Gravity on earth", unit="m/s**2")
        self.add_inward('r0', 6400.0e3, desc="Radius of the Earth", unit="m")

        # outwards
        self.add_outward("g", np.array([0., 0., -10.0]), desc="Gravity", unit="m/s**2")
        self.add_outward("a", np.zeros(3), desc="Acceleration", unit="m/s**2")

        for weight in self.weights:
            self.add_inward(weight, 0.0, desc=f"Weight called {weight}", unit="kg")
        for force in self.forces:
            self.add_inward(force, np.zeros(3), desc=f"Force called {force}", unit="N")

        self.add_outward("force", np.zeros(3), desc="Force", unit="N")
        self.add_outward("weight", 1.0, desc="Weight", unit="kg")

    def compute(self):
        # gravity computation
        r = np.linalg.norm(self.pos)
        u = self.pos / r
        self.g = self.g0 * (self.r0 / r) ** 2 * u 

        self.weight = 0

        for weight in self.weights:
            self.weight += self[weight]

        self.force = self.weight * self.g
        for force in self.forces:
            self.force += self[force]

        self.a = self.force / self.weight