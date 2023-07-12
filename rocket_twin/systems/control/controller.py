from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem

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

    def setup(self, model_path, model_name):

        self.add_inward("time_var", 0.0, desc="System time", unit="")
        self.add_transient("x", der="1")

        fmu_path = create_FMU(model_path, model_name)
        self.add_child(
            FMUSystem("fmu_controller", fmu_path=fmu_path),
            pulling={"w": "w", "ti": "time_var"},
        )

    def compute(self):

        self.time_var = self.time


""
