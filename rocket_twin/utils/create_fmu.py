import os

from OMPython import ModelicaSystem

import rocket_twin.systems.control


def create_FMU(model_path, model_name):
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
