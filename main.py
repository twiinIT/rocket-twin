from Earth import Earth
import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver
import plotly.graph_objs as go
from cosapp.recorders import DataFrameRecorder

#Time-step
dt = 0.01

#Create System
earth = Earth('earth')

#Add RungeKutta driver
driver = earth.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 30)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))


# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Kin.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp']),
    period=1,
)

#Initial conditions and constants

driver.set_scenario(
    init = {
        'Traj.r' : np.zeros(3),
        'Rocket.Kin.v' : np.zeros(3),
        'Rocket.Kin.ar' : np.array([0., np.pi/2 + 0.1, 0.]),
        'Rocket.Kin.av' : 0.*np.array([np.pi/20, np.pi/20, 0.]),
        'Rocket.Geom.Mass.m' : 15.
    })


earth.run_drivers()

# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
mass = np.array(data['Rocket.Dyn.m'])
traj = np.asarray(data['Traj.r'].tolist())
velo = np.asarray(data['Rocket.Kin.v'].tolist())
acel = np.asarray(data['Rocket.Kin.a'].tolist())
thrust = np.asarray(data['Rocket.Thrust.Fp'].tolist())



#Plot results

x=[]
y=[]
z=[]

for i in range(len(traj)):
    x.append(traj[i][0])
    y.append(traj[i][1])
    z.append(traj[i][2])

fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    marker=dict(
        size=4,
        color=z,
        colorscale='Viridis',
    ),
    line=dict(
        color='darkblue',
        width=2
    )
))


fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=2, range=[-500,500],),
        yaxis = dict(nticks=2, range=[-500,500],),
        zaxis = dict(nticks=2, range=[0,1000],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))


fig.show()