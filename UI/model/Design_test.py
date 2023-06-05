from cosapp.base import System
import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver, RunSingleCase
from cosapp.recorders import DataFrameRecorder
from cosapp.tools import problem_viewer
from Cal_coef import Cal_coef
import json

dt = 0.01
coef = Cal_coef('coef')

solver = coef.add_driver(NonLinearSolver('solver', factor = 0.9))
target = solver.add_child(RunSingleCase('target'))
driver = target.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 80)

driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r']),
    period=.1,
)

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
    'Rocket.Kin.ar' : np.array([0, angz, 0]),
    'Rocket.Kin.av' : np.zeros(3),
    'Para.DynPar.r1' : np.array([0., 0., l/2]),
    'Para.DynPar.r2' : np.array([0., 0., l/2]),
    'Para.DynPar.v1' : np.array([0,0,0]),
    'Para.DynPar.v2' : np.array([0,0,0]),
}

if LOAD:
    init = {**init, 
            'Traj.r' : np.array([0,0, rocket_dict['rocket_cog'][0]]),
            'Para.DynPar.r1' : np.array([0., 0., rocket_dict['rocket_cog'][0]]),
            'Para.DynPar.r2' : np.array([0., 0., rocket_dict['rocket_cog'][0]]),
            'Rocket.l' : l,
            'Rocket.Mass.m' : rocket_dict['rocket_mass'],
            'Rocket.Mass.m0' : rocket_dict['rocket_mass'],
            'Rocket.Mass.Dm' : rocket_dict['rocket_prop_weight']/thrust[-1][0],
            'Rocket.Mass.lastEngineTime' : thrust[-1][0],
            'Rocket.Mass.I0_geom' : [rocket_dict['rocket_inertia'][i][i] for i in range(3)],
            'Rocket.Mass.lp' : rocket_dict['motor']['length']*0.001*rocket_dict['motor']['propWeightG']/rocket_dict['motor']['totalWeightG'],
            'Rocket.Mass.Gdm' : rocket_dict['motor']['length']*0.001 + rocket_dict['motor_position'],
            'Rocket.Mass.mCG' : rocket_dict['rocket_mass']*rocket_dict['rocket_cog'][0],

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
            'Para.DynPar.S_ref1' : rocket_dict['parachute_sref1'],
            'Para.DynPar.S_ref2' : rocket_dict['parachute_sref2'],
            'Para.DynPar.AltPara' : rocket_dict['second_para_deploy_alt'],


            'Para.DynPar.Cd' : rocket_dict['parachute_Cd'],

            'Traj.parachute_deploy_method' : 0 if rocket_dict['parachute_deploy_method'] == 'velocity' else 1,
            'Traj.parachute_deploy_timer' : rocket_dict['parachute_deploy_timer'],
            }
    
# print("Initial parameters", init)

driver.set_scenario(
    init = init,
    stop='Para.DynPar.r2[2] < -1'
    )



target.design.add_unknown('eps_cal').add_equation('time == 40.')
target.set_init({'eps_cal': 1.})

coef.run_drivers()

print(coef.eps_cal)

