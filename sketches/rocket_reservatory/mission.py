from vertical_flying_rocket import VerticalFlyingRocket
from fuelling_rocket import FuellingRocket
from cosapp.drivers import Driver
from typing import Optional
from cosapp.systems import System
import pandas as pd

class Mission(Driver):

    def __init__(self,
                 name: str,
                 flux_in,
                 flux_out,
                 dt,
                 owner: Optional['System'] = None,
                 **kwargs):
        
        super().__init__(name, owner, **kwargs)

        #Fuelling
        self.add_child(FuellingRocket('fuelling', flux=flux_in, dt=dt, owner=owner))

        #Flying
        self.add_child(VerticalFlyingRocket('flying', flux=flux_out, dt=dt, owner=owner))

        #Recorder
        self.data = None

    def compute(self):
        super().compute
        for child_name in ["fuelling", "flying"]:
            self.data = pd.concat(
                [self.data, self.children[child_name].rk.recorder.export_data()],
                ignore_index=True,
            )
