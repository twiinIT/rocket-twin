import os
import time

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
        self.add_inward("t0", 0.0, desc="Launch time", unit="")
        self.add_transient("x", der="1")

        pulling = {
            "w": "w",
            "weight": "weight_p",
            "weight_max": "weight_max",
            "t0": "t0",
            "ti": "time_var",
        }

        fmu_path = self.create_fmu(model_path, model_name)
        self.add_child(
            FMUSystem("fmu_controller", fmu_path=fmu_path),
            pulling=pulling,
        )

    def compute(self):

        self.time_var = self.time

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
        time.sleep(3.0)
        for filename in os.listdir(fmu_path):
            if filename != (model_name + ".fmu"):
                os.remove(filename)

        return fmu
