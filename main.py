from Earth import Earth
import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver
import plotly.graph_objs as go
from cosapp.recorders import DataFrameRecorder

#Time-step
dt = 0.1

#Create System
earth = Earth('earth')

#Add RungeKutta driver
driver = earth.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 40)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))


# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Kin.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp', 'Rocket.Kin.Kin_ang']),
    period=1,
)

#Initial conditions and constants

l = 300 #Rocket's length

driver.set_scenario(
    init = {
        'Traj.r' : np.array([0., 0., l/2]),
        'Rocket.Kin.v' : np.zeros(3),
        'Rocket.Kin.ar' : np.array([0., np.pi/2 - 0.1, np.pi/4]),
        'Rocket.Kin.av' : 0*np.array([np.pi/20, np.pi/20, 0.]),
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
ang = np.asarray(data['Rocket.Kin.Kin_ang'].tolist())




#Plot results

x=[]
y=[]
z=[]
theta = []

for i in range(len(traj)):
    x.append(traj[i][0])
    y.append(traj[i][1])
    z.append(traj[i][2])

for i in range(len(ang)):
    theta.append(ang[1])

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
        xaxis = dict(nticks=2, range=[-5000,0],),
        yaxis = dict(nticks=2, range=[-5000,0],),
        zaxis = dict(nticks=2, range=[0,2000],),),
    width=700,
    margin=dict(r=20, l=10, b=10, t=10))


fig.show()


traj_topx = []
traj_topz = []
traj_botx = []
traj_botz = []
traj_topy = []
traj_boty = []

for i in range(len(traj)):
    sign = np.sign(np.pi / 2 - ang[i][1] % 2*np.pi)
    traj_topx.append(traj[i][0] +   l/2 * np.cos(ang[i][1])* np.cos(ang[i][2]))
    traj_botx.append(traj[i][0] -  l/2 * np.cos(ang[i][1])* np.cos(ang[i][2]))
    traj_boty.append(traj[i][1] - l/2 * np.sin(ang[i][2]))
    traj_topy.append(traj[i][1] + l/2 * np.sin(ang[i][2]))
    traj_topz.append(traj[i][2] +  l/2 * np.sin(ang[i][1]))
    traj_botz.append(traj[i][2] -  l/2 * np.sin(ang[i][1]))

traj_topx = np.asarray(traj_topx)
traj_botx = np.asarray(traj_botx)
traj_topz = np.asarray(traj_topz)
traj_botz = np.asarray(traj_botz)

print(traj_topy, traj_boty)

# for i in range(len(traj_top)):
#     print("Traj", (traj_top[i][0]-traj_bot[i][0])**2 + (traj_top[i][1]-traj_bot[i][1])**2)


#Plot results

#Animation - Rocket's movement

fig2 = go.Figure(data=[go.Scatter3d(x=[traj_botx[0], traj_topx[0]], y=[traj_boty[0], traj_topy[0]], z=[traj_botz[0], traj_topz[0]])])

fig2.update_layout(title='Rocket Movement',
                  scene=dict(
            xaxis=dict(range=[-5000, 5000], autorange=False),
            yaxis=dict(range=[-5000, 5000], autorange=False),
            zaxis=dict(range=[0, 3000], autorange=False),
        ),

                  updatemenus=[dict(buttons = [dict(
                                               args = [None, {"frame": {"duration": 100, 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 10}}],
                                               label = "Play",
                                               method = "animate")],
                                type='buttons',
                                showactive=False,
                                y=1,
                                x=1.12,
                                xanchor='right',
                                yanchor='top')])




frames= [go.Frame(data=[go.Scatter3d(x=[traj_botx[i], traj_topx[i]],y = [traj_boty[i], traj_topy[i]], z=[traj_botz[i], traj_topz[i]])]) for i in range(len(traj))]
fig2.update(frames=frames)

fig2.show()