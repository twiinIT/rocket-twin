import json
import matplotlib.pyplot as plt

with open("time_step_simulation.json", "r") as outfile:
    loaded_results = json.load(outfile)

time_steps = loaded_results['time_steps'][:-1]
apogees = loaded_results['apogees'][:-1]
computation_times = loaded_results['computation_times'][:-1]

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