from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.drivers import NonLinearSolver, RunOnce, MonteCarlo, RunSingleCase
from cosapp.utils.distributions import Normal
import sys
sys.path.append('./model')
from Earth import Earth
import json
import numpy as np

earth = Earth("earth")

l = 10 #Rocket's length on the plot
dt = 0.05 #Time-step

angz = -np.pi/2

from cosapp.utils.distributions import Normal
from cosapp.drivers import MonteCarlo
from cosapp.recorders import DataFrameRecorder


LOAD = True

if LOAD:
    with open("./include/init_rocket/rocket_dict.json", "r") as f:
        rocket_dict = json.load(f)
    l = rocket_dict['tube_length'] + rocket_dict['nose_length'] #Rocket's length on the plot
    angz = - rocket_dict['rocket_launch_angle']
    # Load the thrust.txt
    thrust = rocket_dict['motor']['samples']
    with open("model/Utility/thrust.txt", "w") as f:
        for i in range(len(thrust[0])):
            f.write(", ".join([str(point[i]) for point in thrust]))
            if i < len(thrust[0]) - 1:
                f.write("\n")

init = {
    'Traj.r' : np.array([-(l/2)*np.sin(angz), 0., (l/2)*np.cos(angz)]),
    'Rocket.Kin.v' : np.array([0,0,0]),
    'Rocket.Kin.ar' : 'initrot',
    'Rocket.Kin.av' : np.zeros(3),
    'Para.DynPar.r1' : np.array([0., 0., l/2]),
    'Para.DynPar.r2' : np.array([0., 0., l/2]),
    'Para.DynPar.v1' : np.array([0,0,0]),
    'Para.DynPar.v2' : np.array([0,0,0]),
}
# rocket_dict parameters
if LOAD:
    init = {**init, 
            'Traj.r' : np.array([0,0, rocket_dict['rocket_cog'][0]]),
            'Para.DynPar.r1' : np.array([0., 0., rocket_dict['rocket_cog'][0]]),
            'Para.DynPar.r2' : np.array([0., 0., rocket_dict['rocket_cog'][0]]),
            'Rocket.CG': rocket_dict['rocket_cog'][0],
            'Rocket.l' : l,
            'Rocket.Mass.m' : rocket_dict['rocket_mass'],
            'Rocket.Mass.m0' : rocket_dict['rocket_mass'],
            'Rocket.Mass.Dm' : rocket_dict['rocket_prop_weight']/thrust[-1][0],
            'Rocket.Mass.lastEngineTime' : thrust[-1][0],
            'Rocket.Mass.I0_geom' : [rocket_dict['rocket_inertia'][i][i] for i in range(3)],

            'Rocket.Aero.Coefs.ln' : rocket_dict['nose_length'],
            'Rocket.Aero.Coefs.d' : 2*rocket_dict['tube_radius'],
            'Rocket.Aero.Coefs.NFins' : rocket_dict['fins_number'],
            'Rocket.Aero.Coefs.s' : rocket_dict['fins_s'],
            'Rocket.Aero.Coefs.Xt' : rocket_dict['fins_Xt'],
            'Rocket.Aero.Coefs.Cr' : rocket_dict['fins_Cr'],
            'Rocket.Aero.Coefs.Ct' : rocket_dict['fins_Ct'],
            'Rocket.Aero.Coefs.tf' : rocket_dict['fins_thickness'],
            'Rocket.Aero.Coefs.delta' : rocket_dict['delta'],

            'Wind.wind_on' : rocket_dict['wind_on'],
            # 'Wind.wind_average_speed' : rocket_dict['wind_average_speed'],

            'Para.l0' : rocket_dict['parachute_l0'],
            'Para.m1' : rocket_dict['parachute_weight'] + rocket_dict['ejected_nose_mass'],
            'Para.m2' : rocket_dict['rocket_mass'] - rocket_dict['ejected_nose_mass'],
            'Para.DynPar.S_ref' : rocket_dict['parachute_sref'],
            'Para.DynPar.Cd' : rocket_dict['parachute_Cd'],

            'Traj.parachute_deploy_method' : 0 if rocket_dict['parachute_deploy_method'] == 'velocity' else 1,
            'Traj.parachute_deploy_timer' : rocket_dict['parachute_deploy_timer'],
            }
    


def run_analysis(syst, draws=10, linear=True):
    syst.drivers.clear()  # Remove all drivers on the System

    runonce = syst.add_driver(RunOnce("runonce"))
    driver = syst.add_driver(RungeKutta(order=4, dt=dt))
    # driver.add_recorder(DataFrameRecorder(includes=['Rocket.Kin.ar', 'Traj.r', 'initrot']))
    driver.add_child(NonLinearSolver('solver', factor=1.0))
    driver.time_interval = (0, 40)

    # Define a simulation scenario
    driver.set_scenario(
        init = init,
        stop = 'Para.DynPar.r2[2] < -1'
    )

    syst.run_drivers()

    # return driver.recorder.export_data()

    print("MONTECARLO")
    # Montecarlo
    syst.drivers.clear()
    montecarlo = syst.add_driver(MonteCarlo('mc'))
    montecarlo.add_recorder(DataFrameRecorder(includes=['Rocket.Kin.ar', 'Traj.r', 'initrot']))
    montecarlo.add_child(driver)
    montecarlo.draws = draws
    # montecarlo.linear = linear

    # parameters for uncertainties in the data
    pitch_attr = syst.inwards.get_details('pitch_init')
    yaw_attr = syst.inwards.get_details('yaw_init')
    
    # Set the distribution around the current value
    pitch_attr.distribution = Normal(best=.1, worst=-0.02)
    yaw_attr.distribution = Normal(best=.05, worst=-0.05)

    montecarlo.add_random_variable('pitch_init')
    montecarlo.add_random_variable('yaw_init')

    # Computation
    syst.run_drivers()

    return montecarlo.recorder.export_data()



results = run_analysis(earth, draws=6, linear=False)


print(results)


import plotly.graph_objs as go
from plotly.subplots import make_subplots

traj = np.asarray(results['Traj.r'].tolist())

# Create the figure object
fig = make_subplots(rows=1, cols=1)
fig.layout.title = "Probability"
fig.layout.yaxis.title = 'Y Position'

fig.add_trace(
    go.Scatter(
        x=traj[:,0],
        y=traj[:,1],
        mode = 'markers'
    ),
    row = 1,
    col = 1,
)
fig.get_subplot(1, 1).xaxis.title = "X Position"

fig.show()