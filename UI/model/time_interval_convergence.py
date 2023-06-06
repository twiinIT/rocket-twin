import json
import time

import matplotlib.pyplot as plt
import numpy as np
from cosapp.drivers import NonLinearSolver, RungeKutta
from cosapp.recorders import DataFrameRecorder
from Earth import Earth

LOAD = True


def run_simulation(time_step):
    # Time-step
    dt = time_step

    # Create System
    earth = Earth("earth")

    # Add RungeKutta driver
    driver = earth.add_driver(RungeKutta(order=4, dt=dt))
    driver.time_interval = (0, 100)

    # Add NonLinearSolver driver
    solver = driver.add_child(NonLinearSolver("solver", factor=1.0))

    # Add a recorder to capture time evolution in a dataframe
    driver.add_recorder(
        DataFrameRecorder(
            includes=[
                "Traj.r",
                "Rocket.Kin.v",
                "Rocket.Dyn.a",
                "Rocket.Dyn.m",
                "Rocket.Thrust.Fp",
                "Rocket.Kin.Kin_ang",
                "Rocket.Kin.av",
                "Rocket.Aero.F",
                "Traj.v.val",
                "Wind.v_wind.val",
                "Para.DynPar.r1",
                "Para.DynPar.r2",
                "Atmo.Pres.P",
            ]
        ),
        period=0.1,
    )

    # Initial conditions and constants

    l = 2
    angz = -np.pi / 2

    if LOAD:
        with open("./include/init_rocket/rocket_dict.json", "r") as f:
            rocket_dict = json.load(f)
        l = (
            rocket_dict["tube_length"] + rocket_dict["nose_length"]
        )  # Rocket's length on the plot
        angz = -rocket_dict["rocket_launch_angle"]
        # Load the thrust.txt
        thrust = rocket_dict["motor"]["samples"]
        with open("model/Utility/thrust.txt", "w") as f:
            for i in range(len(thrust[0])):
                f.write(", ".join([str(point[i]) for point in thrust]))
                if i < len(thrust[0]) - 1:
                    f.write("\n")

    init = {
        "Traj.r": np.array([-(l / 2) * np.sin(angz), 0.0, (l / 2) * np.cos(angz)]),
        "Rocket.Kin.v": np.array([0, 0, 0]),
        "Rocket.Kin.ar": np.array([0, angz, 0]),
        "Rocket.Kin.av": np.zeros(3),
        "Para.DynPar.r1": np.array([0.0, 0.0, l / 2]),
        "Para.DynPar.r2": np.array([0.0, 0.0, l / 2]),
        "Para.DynPar.v1": np.array([0, 0, 0]),
        "Para.DynPar.v2": np.array([0, 0, 0]),
    }
    # rocket_dict parameters
    if LOAD:
        init = {
            **init,
            "Traj.r": np.array([0, 0, rocket_dict["rocket_cog"][0]]),
            "Para.DynPar.r1": np.array([0.0, 0.0, rocket_dict["rocket_cog"][0]]),
            "Para.DynPar.r2": np.array([0.0, 0.0, rocket_dict["rocket_cog"][0]]),
            "Rocket.l": l,
            "Rocket.Mass.m": rocket_dict["rocket_mass"],
            "Rocket.Mass.m0": rocket_dict["rocket_mass"],
            "Rocket.Mass.Dm": rocket_dict["rocket_prop_weight"] / thrust[-1][0],
            "Rocket.Mass.lastEngineTime": thrust[-1][0],
            "Rocket.Mass.I0_geom": [
                rocket_dict["rocket_inertia"][i][i] for i in range(3)
            ],
            "Rocket.Mass.lp": rocket_dict["motor"]["length"]
            * 0.001
            * rocket_dict["motor"]["propWeightG"]
            / rocket_dict["motor"]["totalWeightG"],
            "Rocket.Mass.Gdm": rocket_dict["motor"]["length"] * 0.001
            + rocket_dict["motor_position"],
            "Rocket.Mass.mCG": rocket_dict["rocket_mass"]
            * rocket_dict["rocket_cog"][0],
            "Rocket.Aero.Coefs.ln": rocket_dict["nose_length"],
            "Rocket.Aero.Coefs.d": 2 * rocket_dict["tube_radius"],
            "Rocket.Aero.Coefs.NFins": rocket_dict["fins_number"],
            "Rocket.Aero.Coefs.s": rocket_dict["fins_s"],
            "Rocket.Aero.Coefs.Xt": rocket_dict["fins_Xt"],
            "Rocket.Aero.Coefs.Cr": rocket_dict["fins_Cr"],
            "Rocket.Aero.Coefs.Ct": rocket_dict["fins_Ct"],
            "Rocket.Aero.Coefs.tf": rocket_dict["fins_thickness"],
            "Rocket.Aero.Coefs.delta": rocket_dict["delta"],
            "Wind.wind_on": rocket_dict["wind_on"],
            # 'Wind.wind_average_speed' : rocket_dict['wind_average_speed'],
            "Para.l0": rocket_dict["parachute_l0"],
            "Para.m1": rocket_dict["parachute_weight"]
            + rocket_dict["ejected_nose_mass"],
            "Para.m2": rocket_dict["rocket_mass"] - rocket_dict["ejected_nose_mass"],
            "Para.DynPar.S_ref": rocket_dict["parachute_sref"],
            "Para.DynPar.Cd": rocket_dict["parachute_Cd"],
            "Traj.parachute_deploy_method": 0
            if rocket_dict["parachute_deploy_method"] == "velocity"
            else 1,
            "Traj.parachute_deploy_timer": rocket_dict["parachute_deploy_timer"],
        }

    driver.set_scenario(init=init, stop="Para.DynPar.r2[2] < -1")

    start_time = time.time()
    earth.run_drivers()
    end_time = time.time()
    computation_time = end_time - start_time

    # Retrieve recorded data
    data = driver.recorder.export_data()
    data = data.drop(["Section", "Status", "Error code"], axis=1)
    r = np.asarray(data["Traj.r"].tolist())
    r1 = np.asarray(data["Para.DynPar.r1"].tolist())
    r2 = np.asarray(data["Para.DynPar.r2"].tolist())

    # find time i where the parachute appears
    time_parachute = 0
    while (
        r1[time_parachute][0] == r2[time_parachute][0]
        and r1[time_parachute][1] == r2[time_parachute][1]
        and r1[time_parachute][2] == r2[time_parachute][2]
    ):
        time_parachute += 1

    r_then_r2 = []
    for i in range(time_parachute):
        r_then_r2.append(r[i])
    for i in range(time_parachute, len(r2)):
        r_then_r2.append(r2[i])

    r_then_r2 = np.array(r_then_r2)

    return np.max(np.array(r_then_r2)[:, 2]), computation_time


time_steps = np.logspace(-2.5, -0.8, num=15)

# Run the simulation for each time step and store the apogee and simulation time
apogees = []
computation_times = []


for time_step in time_steps:
    print("Computing time_step =", time_step, "...")
    apogee, computation_time = run_simulation(time_step)
    apogees.append(apogee)
    computation_times.append(computation_time)

# Plot the apogee depending on the log of the time_step
plt.figure()
plt.semilogx(time_steps, apogees, "o")
plt.xlabel("Time step")
plt.ylabel("Apogee")
plt.title("Apogee vs Time step")
plt.grid()
plt.show()

# Plot the simulation time depending on the log of the time_step
plt.figure()
plt.semilogx(time_steps, computation_times, "o")
plt.xlabel("Time step")
plt.ylabel("Simulation time")
plt.title("Simulation time vs Time step")
plt.grid()
plt.show()


# # Save the results to a JSON file
# results_dict = {
#     "time_steps": time_steps.tolist(),
#     "apogees": apogees,
#     "computation_times": computation_times
# }

# with open("time_step_simulation.json", "w") as outfile:
#     json.dump(results_dict, outfile)
