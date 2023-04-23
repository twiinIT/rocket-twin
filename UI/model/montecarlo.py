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

l = 2 #Rocket's length on the plot
dt = 0.01 #Time-step


from cosapp.utils.distributions import Normal
from cosapp.drivers import MonteCarlo
from cosapp.recorders import DataFrameRecorder


#Initial conditions and constants

rocketNum = 2622
l = 0.855
angz = -np.deg2rad(85)
expCoef = False #True for experimental drag coefficient, false for analytical (possibly innacurate)
Wind = False #True for wind effects, false for no wind
Lift = False #True for lift effects (trajecto does not consider them), false for no lift

init = {
    'Traj.r' : np.array([-(l/2)*np.sin(angz), 0., (l/2)*np.cos(angz)]),
    'Para.DynPar.r1' : np.array([0., 0., l/2]),
    'Para.DynPar.r2' : np.array([0., 0., l/2]),
    'Rocket.CG' : l/2,
    'Rocket.Kin.ar' : np.array([0, angz, 0]),
    'Rocket.Mass.m' : 2.0783,
    'Rocket.Mass.m0' : 2.0783,
    'Rocket.Mass.Dm' : 0.076,
    'Rocket.Mass.lastEngineTime' : 1.,
    'Rocket.Mass.I0_geom' : 1*np.array([1., 100., 100.]),

    'Rocket.Aero.Coefs.ln' : 0.159,
    'Rocket.Aero.Coefs.d' : 0.08,
    'Rocket.Aero.Coefs.NFins' : 4,
    'Rocket.Aero.Coefs.s' : 0.13,
    'Rocket.Aero.Coefs.Xt' : 0.09,
    'Rocket.Aero.Coefs.Cr' : 0.145,
    'Rocket.Aero.Coefs.Ct' : 0.09,
    'Rocket.Aero.Coefs.tf' : 0.002,
    'Rocket.Aero.Coefs.delta' : 0.,

    'Rocket.Aero.Coefs.TypeCd' : expCoef,
    'Wind.wind_on' : Wind,
    'Rocket.Aero.Aeroforces.isLift': Lift,
    'Rocket.Aero.Coefs.Cd_exp': 0.6,

    'Traj.parachute_deploy_method' : 0,
    'Traj.parachute_deploy_timer' : 0.,

}

def run_analysis(syst, draws=10, linear=True):
    syst.drivers.clear()  # Remove all drivers on the System

    # runonce = syst.add_driver(RunOnce("runonce"))
    driver = syst.add_driver(RungeKutta(order=4, dt=dt))
    driver.add_recorder(DataFrameRecorder(includes=['Rocket.Kin.ar', 'Traj.r', 'Rocket.Kin.v', 'initrot', 'Rocket.Thrust.inclinaison']), period=0.1)
    driver.add_child(NonLinearSolver('solver', factor=1.0))
    driver.time_interval = (0, 70)

    # Define a simulation scenario
    driver.set_scenario(
        init = init,
        stop = 'Para.DynPar.r2[2] < -1'
    )

    syst.run_drivers()

    return driver.recorder.export_data()

    print("MONTECARLO")
    # Montecarlo
    syst.drivers.clear()
    montecarlo = syst.add_driver(MonteCarlo('mc'))
    montecarlo.add_recorder(DataFrameRecorder(includes=['Rocket.Kin.ar', 'Traj.r', 'initrot', 'Traj.v.val', 'Rocket.Thrust.inclinaison']))
    montecarlo.add_child(driver)
    montecarlo.draws = draws
    # montecarlo.linear = linear

    # parameters for uncertainties in the data
    pitch_attr = syst.inwards.get_details('pitch_init')
    yaw_attr = syst.inwards.get_details('yaw_init')
    bang_attr = syst.Rocket.Thrust.inwards.get_details('inclinaison')
    
    # Set the distribution around the current value
    pitch_attr.distribution = Normal(best=.02, worst=-.02)
    yaw_attr.distribution = Normal(best=.02, worst=-.02)
    bang_attr.distribution = Normal(best=.01, worst=-0.01)

    montecarlo.add_random_variable('pitch_init')
    montecarlo.add_random_variable('yaw_init')
    montecarlo.add_random_variable('Rocket.Thrust.inclinaison')

    # Computation
    syst.run_drivers()

    return montecarlo.recorder.export_data()



results = run_analysis(earth, draws=2, linear=False)

print(results)