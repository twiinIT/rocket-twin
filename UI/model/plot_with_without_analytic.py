import json 
import matplotlib.pyplot as plt
import numpy as np

with open("2623_3.json", "r") as outfile:
    given_coef = json.load(outfile)

with open("2623_4.json", "r") as outfile:
    analytic_coef = json.load(outfile)

r_then_r2_given = given_coef['r_then_r2']
r_then_r2_analytic = analytic_coef['r_then_r2']

time_given = given_coef['time']
pres_given = given_coef['pressure']

time_analytic = analytic_coef['time']
pres_analytic = analytic_coef['pressure']

#time_pres = given_coef['time_pres']
#exp_pres = given_coef['exp_pres']

time_alt = given_coef['time_alt']
exp_alt = given_coef['exp_alt']

time_traj = given_coef['time_traj']
exp_traj = given_coef['exp_traj']

# Interpolate data points to have the same length
max_time = max(max(time_given), max(time_analytic))
time_common = np.linspace(0, max_time, num=max(len(time_given), len(time_analytic)))

r_then_r2_given_interp = np.interp(time_common, time_given, np.array(r_then_r2_given)[:, 2])
r_then_r2_analytic_interp = np.interp(time_common, time_analytic, np.array(r_then_r2_analytic)[:, 2])

pres_given_interp = np.interp(time_common, time_given, pres_given)
pres_analytic_interp = np.interp(time_common, time_analytic, pres_analytic)

print('\n')
print('FOR ANALYTIC Cd:')
print('\n')
print("Apogee Height: ", np.max(np.array(r_then_r2_analytic)[:,2]), "m")
print('\n')
print("Total Flight Time: ", time_analytic[-1], "s")
print('\n')
print("Landing Point: ", np.array(r_then_r2_analytic)[-1,0], "m")
print('\n')
print("Lowest Pressure", np.min(pres_analytic), "Pa")
print('\n')

print('\n')
print('FOR GIVEN Cd:')
print('\n')
print("Apogee Height: ", np.max(np.array(r_then_r2_given)[:,2]), "m")
print('\n')
print("Total Flight Time: ", time_given[-1], "s")
print('\n')
print("Landing Point: ", np.array(r_then_r2_given)[-1,0], "m")
print('\n')
print("Lowest Pressure", np.min(pres_given), "Pa")
print('\n')

plt.plot(time_common, r_then_r2_given_interp, label='Model Prediction for given coefficient')
plt.plot(time_common, r_then_r2_analytic_interp, label='Model Prediction for analytic coefficient')
plt.plot(time_alt, exp_alt, label='Experimental Curve')
plt.title("Rocket Altitude")
plt.xlabel("Time (s)")
plt.ylabel("Height (m)")
plt.legend()
plt.show()

plt.plot(np.array(r_then_r2_given)[:,0], np.array(r_then_r2_given)[:,2], label = 'Model Prediction for given coefficient')
plt.plot(np.array(r_then_r2_analytic)[:,0], np.array(r_then_r2_analytic)[:,2], label = 'Model Prediction for analytic coefficient')
plt.plot(time_traj, exp_traj, label = "Trajecto Prediction")
plt.title("Rocket XZ Trajectory")
plt.xlabel("Horizontal Displacement (m)")
plt.ylabel("Height (m)")
plt.legend()
plt.show()

plt.plot(time_given, pres_given, label = "Model Prediction for given coefficient")
plt.plot(time_analytic, pres_analytic, label = "Model Prediction for analytic coefficient")
#plt.plot(time_pres, exp_pres, label = "Experimental Curve")
plt.title("Pressure over Time")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (Pa)")
plt.legend()
plt.show()
