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

    def __init__(
        self,
        name: str,
        owner: Optional["System"] = None,
        init: Optional[dict] = None,
        stop: Optional[str] = None,
        dt: Optional[float] = 0.1,
        includes: Optional[list[str]] = None,
        **kwargs
    ):
        super().__init__(name, owner, **kwargs)

        # Init and stop conditions
        init_fuel = init
        init_flight = {
            "rocket.engine.switch": True,
            "rocket.tank.w_out_temp": 3.0,
            "g_tank.w_in": 0.0,
            "g_tank.is_open": False,
        }

        stop_fuel = "rocket.tank.weight_p >= rocket.tank.weight_max"
        stop_flight = stop

        # Fueling
        self.add_child(
            FuelingRocket(
                "fr", owner=owner, init=init_fuel, stop=stop_fuel, includes=includes, dt=dt
            )
        )

        # Flying
        self.add_child(
            VerticalFlyingRocket(
                "vfr", owner=owner, init=init_flight, stop=stop_flight, includes=includes, dt=dt
            )
        )

        # Recorder
        self.data = None

    def compute(self):
        for child in self.children.values():
            self.data = pd.concat(
                [self.data, child.rk.recorder.export_data()],
                ignore_index=True,
            )
