from Earth import Earth
import numpy as np
from cosapp.drivers import RungeKutta
import plotly.graph_objs as go
from cosapp.recorders import DataFrameRecorder

earth = Earth('earth')
driver = earth.add_driver(RungeKutta(order=3, dt=0.05))
driver.time_interval = (0,40)

# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['r', 
    'v.vector', 
    'a',
    'norm(v.vector)', 
    'theta', 'm']),
    period=0.05 ,
)

# Define a simulation scenario
driver.set_scenario(
    init = {
        'r': np.zeros(2),
        'theta': np.pi/2 - 0.1
    },
    values = {
        'm': 15,
    },
    stop = 'r[1] < 0'
)

earth.run_drivers()

# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
mass = np.array(data['m'])
time = np.asarray(data['time'])
traj = np.asarray(data['r'].tolist())
traj_angle = np.asarray(data['theta'].tolist())

l = 20 #Rocket's length

semi_length = np.transpose((l/2) * np.array([np.cos(traj_angle), np.sin(traj_angle)]))

traj_top = []
traj_bot = []

for i in range(len(traj)):
    sign = np.sign(np.pi / 2 - traj_angle[i])
    traj_top.append(traj[i] + sign * semi_length[i])
    traj_bot.append(traj[i] - sign * semi_length[i])

traj_top = np.asarray(traj_top)
traj_bot = np.asarray(traj_bot)
# for i in range(len(traj_top)):
#     print("Traj", (traj_top[i][0]-traj_bot[i][0])**2 + (traj_top[i][1]-traj_bot[i][1])**2)


#Plot results

#Animation - Rocket's movement

fig2 = go.Figure(go.Scatter(x=[traj_bot[0][0], traj_top[0][0]], y=[traj_bot[0][1], traj_top[0][1]]))

fig2.update_layout(title='Rocket Movement',
                  title_x=0.5,
                  width=600, height=600, 
                  xaxis_title='Ground Level', 
                  yaxis_title='Height',
                  yaxis_range=(-10,1000),
                  xaxis_range=(-505,505), #you generate y-values for i =0, ...99, 
                                      #that are assigned, by default, to x-values 0, 1, ..., 99
                  
                  updatemenus=[dict(buttons = [dict(
                                               args = [None, {"frame": {"duration": 100*0.05, 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 0}}],
                                               label = "Play",
                                               method = "animate")],
                                type='buttons',
                                showactive=False,
                                y=1,
                                x=1.12,
                                xanchor='right',
                                yanchor='top')])


                                          
                    
frames= [go.Frame(data=[go.Scatter(x=[traj_bot[i,0], traj_top[i,0]],y=[traj_bot[i,1], traj_top[i,1]])]) for i in range(len(traj))]
fig2.update(frames=frames)

fig2.show()



#Theta angle 

traj_angle *= 180/np.pi

traces = [
    go.Scatter(
        x = time,
        y = traj_angle,
        mode = 'lines',
        name = 'numerical',
        line = dict(color='red'),
    )
   
]
layout = go.Layout(
    title = "Trajectory",
    xaxis = dict(title="time"),
    yaxis = dict(
        title = "theta",
    ),
    hovermode = "x",
)

fig = go.Figure(data=traces, layout=layout)
fig.show()




#Rocket' trajectory
# import matplotlib.pyplot as plt

# # Matplotlib vizualisation
# plt.plot([traj[i,0] for i in range(len(traj))], [traj[i,1] for i in range(len(traj))], 'r')
# plt.xlabel("x (m)")
# plt.ylabel("z (m)")

# plt.title("Trajectoire du modèle 2D")
# plt.show()

traces3 = [
    go.Scatter(
        x = [traj[i,0] for i in range(len(traj))],
        y = [traj[i,1] for i in range(len(traj))],
        mode = 'lines',
        name = 'numerical',
        line = dict(color='red'),
    )
   
]
layout3 = go.Layout(
    title = "Trajectory",
    xaxis = dict(title="x (m)"),
    yaxis = dict(
        title = "z (m)",
    ),
    hovermode = "x",
)

fig3 = go.Figure(data=traces3, layout=layout3)
fig3.show()

print("Apogee : ", np.max(traj[:,1]), "m")


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