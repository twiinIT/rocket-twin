import os

from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem
from OMPython import ModelicaSystem

import rocket_twin.systems.control


class StageControllerFMU(System):
    """Controller of the command variables.

    Inputs
    ------
    model_path: string,
        the path to the .mo file, if any
    model_name: string,
        the .fmu file name
    is_on: boolean,
        whether the system is in fueling phase or not
    weight_prop: float,
        stage fuel weight
    weight_max: float,
        stage maximum fuel weight

    Outputs
    ------
    w: float,
        command flux
    """

    def setup(self, model_path, model_name):

        self.add_inward("weight_prop", 0.0, desc="Stage propellant weight", unit="kg")
        self.add_inward("weight_max", 1.0, desc="Stage maximum propellant weight", unit="kg")
        self.add_inward("is_on", False, desc="Whether the stage is on or not")

        fmu_path = self.create_fmu(model_path, model_name)
        self.add_child(
            FMUSystem("fmu_controller", fmu_path=fmu_path),
            pulling=['is_on', 'w'],
        )

        self.add_event("full", trigger="weight_prop == weight_max")

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