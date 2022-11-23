from Rocket import Rocket
import numpy as np
from cosapp.drivers import RungeKutta
import plotly.graph_objs as go
import plotly.figure_factory as ff
from cosapp.recorders import DataFrameRecorder

rocket = Rocket('rocket')
driver = rocket.add_driver(RungeKutta(order=4, dt=0.1))
driver.time_interval = (0,40)

# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['r', 'V', 'a', 'norm(V)', 'theta', 'm', 'F']),
    period=0.05,
)

# Define a simulation scenario
driver.set_scenario(
    init = {
        'r': np.zeros(2),
        'V': np.zeros(2),
        'theta': np.pi/2 + 0.00001
    },
    values = {
        'm': 15,
    },


)

rocket.run_drivers()

# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
mass = np.array(data['m'])
thrust = np.array(data['F'])
theta = np.array(data['theta'])
time = np.asarray(data['time'])
angle = np.asarray(data['theta'])
traj = np.asarray(data['r'].tolist())
print("dn")
print(theta)


#Plot results

traces = [
    go.Scatter(
        x = traj[:, 0],
        y = traj[:, 1],
        mode = 'lines',
        name = 'numerical',
        line = dict(color='red'),
    )
   
]
layout = go.Layout(
    title = "Trajectory",
    xaxis = dict(title="x"),
    yaxis = dict(
        title = "z",
        scaleanchor = "x",
        scaleratio = 1,
    ),
    hovermode = "x",
)

fig = go.Figure(data=traces, layout=layout)
fig.show()






# fig =  ff.create_quiver(
#         traj[:, 0], 
#         traj[:, 1], 
#         np.cos(angle), 
#         np.sin(angle),
#         scale=5,
#         arrow_scale=.4,
#         name='quiver',
#         line_width=1)

# fig.update_layout(title='Trajectoire de la fusée', yaxis=dict(scaleanchor="x", scaleratio=1)) 

# fig.show()