from cosapp.base import System


class Pipe(System):
    """A simple model of a pipe.

    Inputs
    ------
    w_in [kg/s]: float,
        mass flow of fuel entering the pipe
    is_open: boolean,
        whether the pipe is open or closed

    Outputs
    ------
    w_out [kg/s]: floatm
        mass flow of fuel exiting the pipe
    """

    def setup(self):

        self.add_inward("is_open", False, desc="Whether the pipe is open or not", unit='')
        self.add_inward("w_in", 0.0, desc="Fuel income rate", unit="kg/s")

        self.add_outward("w_out", 0.0, desc="Fuel exit rate", unit="kg/s")

    def compute(self):

        if self.is_open == False:
            self.parent.g_tank.w_out_temp = 0.
        self.w_out = self.w_in