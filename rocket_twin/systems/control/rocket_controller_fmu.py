import os

from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem
from OMPython import ModelicaSystem

import rocket_twin.systems.control


class RocketControllerFMU(System):
    """Controller of the command variables.

    Inputs
    ------
    model_path: string,
        the path to the .mo file, if any
    model_name: string,
        the .fmu file name
    flying: boolean,
        whether the rocket is mid-flight or not
    n_stages: int,
        rocket's number of stages
    weight_prop_i: float,
        i-th stage fuel weight

    Outputs
    ------
    is_on_i: boolean,
        whether the i-th stage controller is active or not
    """

    def setup(self, n_stages, model_path, model_name):

        self.add_inward("n_stages", n_stages, desc="number of stages")
        self.add_inward("stage", 1, desc="Current active stage")

        pulling = {"flying": "flying"}

        for i in range(1, n_stages + 1):
            self.add_outward(f"is_on_{i}", 0, desc=f"Whether the stage {i} is on or not")
            pulling[f"weight_{i}"] = f"weight_prop_{i}"
            pulling[f"is_on_{i}"] = f"is_on_{i}"

        fmu_path = self.create_fmu(model_path, model_name)
        self.add_child(
            FMUSystem("fmu_controller", fmu_path=fmu_path),
            pulling=pulling,
        )

        self.add_event("drop", trigger="weight_prop_1 < 0.1")

    def compute(self):

        for i in range(1, self.n_stages):
            self[f"is_on_{i}"] = bool(self[f"is_on_{i}"])

    def transition(self):

        if self.drop.present:
            if self.stage < self.n_stages:
                self.stage += 1
                self.drop.trigger = f"weight_prop_{self.stage} < 0.1"

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
