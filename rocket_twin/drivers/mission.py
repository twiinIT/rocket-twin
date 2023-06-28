from typing import Optional

import pandas as pd
from cosapp.drivers import Driver
from cosapp.systems import System

from rocket_twin.drivers.fueling_rocket import FuelingRocket
from rocket_twin.drivers.vertical_flying_rocket import VerticalFlyingRocket


class Mission(Driver):
    """Driver that simulates the fueling and the vertical flight of a rocket.

    Inputs
    ------
    name: string,
        the name of the driver
    w_in [kg/s]: float,
        mass flow of fuel entering the rocket tank during refueling
    w_out [kg/s]: float,
        mass flow of fuel exiting the rocket tank during flight
    dt [s]: float,
        integration time step
    owner: System,
        the system that owns the driver

    Outputs
    ------
    """

    def __init__(self, name: str, w_in, w_out, dt, owner: Optional["System"] = None, **kwargs):
        super().__init__(name, owner, **kwargs)

        # Fuelling
        self.add_child(FuelingRocket("fuelling", w_out=w_in, dt=dt, owner=owner))

        # Flying
        self.add_child(VerticalFlyingRocket("flying", w_out=w_out, dt=dt, owner=owner))

        # Recorder
        self.data = None

    def compute(self):
        super().compute
        for child_name in ["fuelling", "flying"]:
            self.data = pd.concat(
                [self.data, self.children[child_name].rk.recorder.export_data()],
                ignore_index=True,
            )
