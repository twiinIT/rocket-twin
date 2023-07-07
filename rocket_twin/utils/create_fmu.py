import os
import rocket_twin.systems.control
from OMPython import ModelicaSystem

def create_FMU(model_path, model_name):

    fmu_path = os.path.join(rocket_twin.systems.control.__path__[0], model_name)
    try:
        os.mkdir(fmu_path)
    except OSError:
        pass
    os.chdir(fmu_path)
    mod=ModelicaSystem(model_path,model_name)
    fmu =  mod.convertMo2Fmu()
    for filename in os.listdir(fmu_path):
        if filename != (model_name + ".fmu"):
            os.remove(filename)

    return fmu