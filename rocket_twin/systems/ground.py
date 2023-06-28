from cosapp.base import System


class Ground(System):
    """Ground system that manages the stations.

    Inputs
    ------
    stations : System,
        space stations

    Outputs
    ------
    """

    def setup(self, stations=None):

        if stations is None:
            stations = []

        self.add_property("stations", stations)

        for station in stations:

            self.add_child(station)
