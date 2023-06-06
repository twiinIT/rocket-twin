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

    def setup(self, forces=None, weights=None, centers=None):
        if forces is None:
            forces = []
        if weights is None:
            weights = []
        if centers is None:
            centers = []

        self.add_property("forces", forces)
        self.add_property("weights", weights)
        self.add_property("centers", centers)

        self.add_inward("g", -10.0, desc="Gravity", unit="m/s**2")

        self.add_outward("a", 0.0, desc="Acceleration", unit="m/s**2")

        for weight in self.weights:
            self.add_inward(weight, 0.0, desc=f"Weight called {weight}", unit="kg")
        for force in self.forces:
            self.add_inward(force, 0.0, desc=f"Force called {force}", unit="N")
        for center in self.centers:
            self.add_inward(center, 0.0, desc=f"Center of gravity of the {center}", unit="m")

        self.add_outward("force", 1.0, desc="Force", unit="N")
        self.add_outward("weight", 1.0, desc="Weight", unit="kg")
        self.add_outward("center", 1.0, desc="Center of gravity", unit="m")

    def compute(self):
        self.weight = 0
        self.center = 0
        for i in range(len(self.centers)):
            self.center += self[self.centers[i]] * self[self.weights[i]]
            self.weight += self[self.weights[i]]

        self.center /= self.weight

        self.force = self.weight * self.g
        for force in self.forces:
            self.force += self[force]

        self.a = self.force / self.weight
