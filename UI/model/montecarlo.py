from cosapp.drivers import RungeKutta
from cosapp.recorders import DataFrameRecorder
from cosapp.drivers import NonLinearSolver, RunOnce, MonteCarlo, RunSingleCase
from cosapp.utils.distributions import Normal
from Earth import Earth
import numpy as np

earth = Earth("earth")

l = 10 #Rocket's length on the plot
dt = 0.05 #Time-step


from cosapp.utils.distributions import Normal
from cosapp.drivers import MonteCarlo
from cosapp.recorders import DataFrameRecorder

def run_analysis(syst, draws=10, linear=True):
    syst.drivers.clear()  # Remove all drivers on the System

    runonce = syst.add_driver(RunOnce("runonce"))
    driver = syst.add_driver(RungeKutta(order=4, dt=dt))
    driver.add_child(NonLinearSolver('solver', factor=1.0))
    driver.time_interval = (0, 40)

    # Define a simulation scenario
    driver.set_scenario(
        init = {
        'Traj.r' : np.array([0., 0., l/2]),
        'Rocket.Kin.v' : np.array([0,0,0]),
        # 'Rocket.Kin.ar' : np.array([0., -np.pi/2 + 0.1, 0.0]),
        'Rocket.Kin.av' : np.zeros(3),
        'Para.DynPar.r1' : np.array([0., 0., l/2]), #(should be l because the parachute is at the tip of the rocket)
        'Para.DynPar.r2' : np.array([0., 0., l/2]),
        'Para.DynPar.v1' : np.array([0,0,0]),
        'Para.DynPar.v2' : np.array([0,0,0]),
        'Traj.ParaDepStatus': False,
        'yaw_init': 0.1,
        'pitch_init': 0.1,
        'Rocket.Kin.ar' : 'ar_0',
    },
    stop='Para.DynPar.r1[2] < -1'
    )

    syst.run_drivers()
    print("MONTECARLO")
    # Montecarlo
    syst.drivers.clear()
    montecarlo = syst.add_driver(MonteCarlo('mc'))
    montecarlo.add_recorder(DataFrameRecorder(includes=['Rocket.Kin.ar', 'Traj.r']))
    montecarlo.add_child(driver)
    montecarlo.draws = draws
    # montecarlo.linear = linear

    # parameters for uncertainties in the data
    pitch_attr = syst.inwards.get_details('pitch_init')
    yaw_attr = syst.inwards.get_details('yaw_init')
    # Set the distribution around the current value
    pitch_attr.distribution = Normal(best=.05, worst=-0.05)
    yaw_attr.distribution = Normal(best=.05, worst=-0.05)

    montecarlo.add_random_variable('pitch_init')
    montecarlo.add_random_variable('yaw_init')

    # Computation
    syst.run_drivers()

    return montecarlo.recorder.export_data()


results = run_analysis(earth, draws=2, linear=False)


import plotly.graph_objs as go
from plotly.subplots import make_subplots

traj = np.asarray(results['Traj.r'].tolist())
print(traj[:, 0])

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