from rocket_twin.systems import Station, ControllerFMU
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from cosapp.utils import swap_system
import numpy as np
import matplotlib.pyplot as plt

model_path = r"systems\control\controller.mo"
model_name = "controller"

model_path_r = r"systems\control\rocket_controller.mo"
model_name_r = "rocket_controller"

sys = Station("sys")
swap_system(
    sys.controller,
    ControllerFMU("controller", model_path=model_path, model_name=model_name),
)
swap_system(
    sys.rocket.controller,
    ControllerFMU("controller", model_path=model_path_r, model_name=model_name_r),
)

sys.connect(sys.controller.inwards, sys.rocket.inwards, ["weight_max", "weight_p"])
sys.rocket.connect(
    sys.rocket.controller.inwards, sys.rocket.tank.inwards, ["weight_max", "weight_p"]
)

driver = sys.add_driver(RungeKutta(order=4, time_interval=[0, 25], dt=0.01))
solver = driver.add_child(NonLinearSolver('solver'))
init = {"g_tank.weight_p": 10.0, "rocket.tank.weight_p": 0.0}
values = {
    "g_tank.w_out_max": 1.0,
    "rocket.tank.w_out_max": 0.5,
    "controller.time_int": 10.,
    "rocket.controller.time_int": 10.,
}

includes = ["rocket.tank.weight_p", "g_tank.weight_p", "rocket.a"]

driver.set_scenario(init=init, values=values)
driver.add_recorder(DataFrameRecorder(includes=includes), period=1.0)

sys.run_drivers()
data = driver.recorder.export_data()

time = np.asarray(data['time'])
g_mass = np.asarray(data["g_tank.weight_p"])
r_mass = np.asarray(data["rocket.tank.weight_p"])
acel = np.asarray(data['rocket.a'])

plt.plot(time, g_mass, label="Ground tank fuel mass")
plt.plot(time, r_mass, label="Rocket tank fuel mass")
plt.title("Ground and rocket fuel masses over time")
plt.xlabel("Time (s)")
plt.ylabel("Mass (kg)")
plt.legend()
plt.show()

plt.plot(time, acel, label="Rocket acceleration")
plt.title("Rocket acceleration over time")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.legend()
plt.show()

from cosapp.base import System

from rocket_twin.systems import Dynamics, Stage


class Rocket(System):
    """A simple model of a rocket.

    Inputs
    ------
    n_stages: int,
        how many stages the rocket has
    flying: boolean,
        whether the rocket is already flying or still on ground

    Outputs
    ------
    """

    def setup(self):


        self.add_inward("n_stages", 1, desc="Number of rocket stages", unit='')

        forces, weights, centers = ([] for i in range(self.n_stages))

        for i in range(self.n_stages):
            self.add_child(Stage(f"stage_{i}"))
            forces[i] = f"thrust_{i}"
            weights[i] = f"weight_{i}"
            centers[i] = f"center_{i}"

        self.add_child(
            Dynamics(
                "dyn",
                forces=forces,
                weights=weights,
                centers=centers,
            ),
            pulling=["a"],
        )

        for stage in self.children:
            if stage != "dyn":
                self.connect(
                    self.stage.outwards,
                    self.dyn.inwards,
                    {"force": f"thrust_{i}", "weight": f"weight_{i}", "center": f"center_{i}"},
                )

        
        self.add_inward_modevar(
            "flying", False, desc="Whether the rocket is flying or not", unit=""
        )

        self.add_event("Takeoff", trigger="dyn.a > 0")

    def compute(self):
        self.a *= self.flying

    def transition(self):

        if self.Takeoff.present:
            self.flying = True