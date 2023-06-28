from cosapp.base import System


class RocketGeom(System):
    """Calculates the necessary geometric parameters of a rocket.

    Inputs
    ------
    centers [m]: float,
        center of gravity of each component of the rocket
    weights [kg]: float,
        weight of each component of the rocket

    Outputs
    ------
    center [m]: float,
        center of gravity of the rocket
    """

    def setup(self, centers=None, weights=None):
        if centers is None:
            centers = []
        if weights is None:
            weights = []

        self.add_property("centers", centers)
        self.add_property("weights", weights)

        self.add_outward("center", 1.0, desc="Center of gravity", unit="m")

        for center in self.centers:
            self.add_inward(center, 0.0, desc=f"Center of gravity of the {center}", unit="m")
        for weight in self.weights:
            self.add_inward(weight, 0.0, desc=f"Weight called {weight}", unit="kg")

    def compute(self):
        self.center = 0
        weight = 0
        for i in range(len(self.centers)):
            self.center += self[self.centers[i]] * self[self.weights[i]]
            weight += self[self.weights[i]]

        self.center /= weight
