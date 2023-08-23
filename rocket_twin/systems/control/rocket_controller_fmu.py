import os

from cosapp.base import System
from cosapp_fmu.FMUsystem import FMUSystem
from OMPython import ModelicaSystem

import rocket_twin.systems.control

class RocketControllerFMU(System):

    def setup(self, n_stages, model_path, model_name):

        self.add_inward("n_stages", n_stages, desc="number of stages")
        self.add_inward("stage", 1, desc="Current active stage")

        self.add_inward("time_var", 0.0, desc="System time", unit="")
        self.add_inward("time_int", 0.0, desc="Interval between fueling end and launch", unit="")
        self.add_inward("time_lnc", 100000.0, desc="Launch time", unit="")
        self.add_transient("x", der="1")

        pulling = {"flying" : "flying", "fueling" : "fueling", "tl" : "time_lnc", "ti" : "time_var"}

        for i in range(1, n_stages + 1):
            self.add_outward(f"is_on_{i}", 0, desc=f"Whether the stage {i} is on or not")
            pulling[f"weight_{i}"] = f"weight_prop_{i}"
            pulling[f"weight_max_{i}"] = f"weight_max_{i}"
            pulling[f"is_on_{i}"] = f"is_on_{i}"

        fmu_path = self.create_fmu(model_path, model_name)
        self.add_child(
            FMUSystem("fmu_controller", fmu_path=fmu_path),
            pulling=pulling,
        )

        self.add_event("full", trigger = "weight_prop_1 > 0.9999*weight_max_1")
        self.add_event("drop", trigger="weight_prop_1 < 0.1")

    def compute(self):

        self.time_var = self.time

    def transition(self):

        if self.full.present:
            if self.stage < self.n_stages:
                self.stage += 1
                self.full.trigger = f"weight_prop_{self.stage} > 0.9999 * weight_max_{self.stage}"
            else:
                self.time_lnc = self.time + self.time_int
                self.stage = 1
        
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


