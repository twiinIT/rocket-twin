from cosapp.base import System


class Dynamics(System):
    """Dynamics of a physical system.

    Inputs
    ------
    forces [N]: float,
        total force in each component of the system
    weights [kg]: float,
        total weight of each component of the system

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

        self.add_inward("switch", False, desc="Whether rocket is on or off")
        self.add_inward("g", -10.0, desc="Gravity", unit="m/s**2")

        self.add_outward("a", 1.0, desc="Acceleration", unit="m/s**2")

        for weight in self.weights:
            self.add_inward(weight, 0.0, desc=f"Weight called {weight}", unit="kg")
        for force in self.forces:
            self.add_inward(force, 0.0, desc=f"Force called {force}", unit="N")

        self.add_outward("force", 1.0, desc="Force", unit="N")
        self.add_outward("weight", 1.0, desc="Weight", unit="kg")

    def compute(self):
        self.weight = 0
        for weight in self.weights:
            self.weight += self[weight]

        if self.switch:
            self.force = self.weight * self.g
            for force in self.forces:
                self.force += self[force]

        else:
            self.force = 0.0

        self.a = self.force / self.weight
