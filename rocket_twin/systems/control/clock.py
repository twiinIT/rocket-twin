from cosapp.base import System


class Clock(System):
    """A system that measures the elapsed time.

    Inputs
    ------

    Outputs
    ------
    time_var: float,
        the time since the beginning of the simulation
    """

    def setup(self):

        # Transient to ensure the system is visited in every time step
        self.add_transient("x", der="1")
        self.add_outward("time_var", 0.0, desc="Command time")

    def compute(self):

        self.time_var = self.time
