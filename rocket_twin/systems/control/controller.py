from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem

from rocket_twin.systems.control import CosappController
from rocket_twin.utils import create_FMU


class Controller(System):
    """Controller of the command variables.

    Inputs
    ------
    model_path: string,
        the path to the .mo file, if any
    model_name: string
        the .fmu file name

    Outputs
    ------
    'f': float,
        command force
    'wr': float,
        command flow
    'wg' float,
        command flow
    """

    def setup(self, model_path=None, model_name=None):

        self.add_inward("time_var", 0.0, desc="System time", unit="")
        self.add_transient("x", der="1")

        if model_path is None:
            self.add_child(CosappController("cos_control"), pulling=["f", "wr", "wg"])
        else:
            fmu_path = create_FMU(model_path, model_name)
            self.add_child(
                FMUSystem("fmu_controller", fmu_path=fmu_path),
                pulling={"f": "f", "wr": "wr", "wg": "wg", "ti": "time_var"},
            )

    def compute(self):

        self.time_var = self.time


""
