import os

from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem
from OMPython import ModelicaSystem

import rocket_twin.systems.control


class ControllerFMU(System):
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
        self.add_inward("time_int", 0.0, desc="Interval between fueling end and launch", unit="")
        self.add_inward("time_lnc", 100000.0, desc="Launch time", unit="")
        self.add_transient("x", der="1")

        pulling = {
            "w": "w",
            "weight": "weight_p",
            "weight_max": "weight_max",
            "tl": "time_lnc",
            "ti": "time_var",
        }

        fmu_path = self.create_fmu(model_path, model_name)
        self.add_child(
            FMUSystem("fmu_controller", fmu_path=fmu_path),
            pulling=pulling,
        )

        self.add_event("full_tank", trigger="weight_p > 0.9999*weight_max")

    def compute(self):

        self.time_var = self.time

    def transition(self):

        if self.full_tank.present:

            self.time_lnc = self.time_var + self.time_int

    def create_fmu(self, model_path, model_name):
        """Create an fmu file in the control folder from an mo file.

        Inputs
        ------
        model_path: string
            the path of the .mo file
        model_name: string
            the name of the .fmu file to be created

        Outputs
        ------

        fmu: string
            the path to the .fmu file
        """

        fmu_path = os.path.join(rocket_twin.systems.control.__path__[0], model_name)
        model_path = os.path.join(rocket_twin.__path__[0], model_path)
        model_path = model_path.replace("\\", "/")
        try:
            os.mkdir(fmu_path)
        except OSError:
            pass
        os.chdir(fmu_path)
        mod = ModelicaSystem(model_path, model_name)
        fmu = mod.convertMo2Fmu()
        for filename in os.listdir(fmu_path):
            if filename != (model_name + ".fmu"):
                os.remove(filename)

        return fmu
