from cosapp.base import System


class Ground(System):
    """Ground system that manages the stations.

    Inputs
    ------
    stations : List[System],
        space stations

    Outputs
    ------
    """

    def setup(self, stations=None):

        if stations is None:
            stations = []

        for station in stations:

            self.add_child(station)
