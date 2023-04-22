from Earth import Earth
import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from scipy.spatial.transform import Rotation as R
import json
import IPython

# Set the matplotlib backend to 'qt' for the jupyter notebook
# The condition checks if the script is run using IPython
if IPython.get_ipython() is not None:
    IPython.get_ipython().run_line_magic('matplotlib', 'qt')

LOAD = True

#Time-step
dt = 0.05

#Create System
earth = Earth('earth')

#Add RungeKutta driver
driver = earth.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 50)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))

# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Dyn.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp', 'Rocket.Kin.Kin_ang',
                                 'Rocket.Kin.av', 'Rocket.Aero.F', 'Traj.v.val', 'Wind.v_wind.val', 'Para.DynPar.r1', 'Para.DynPar.r2', 'Atmo.Pres.P']),
    period=.1,
)

#Initial conditions and constants

l = 2
angz = -np.pi/2

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
    
# print("Initial parameters", init)

driver.set_scenario(
    init = init,
    stop='Para.DynPar.r2[2] < -1'
    )


earth.run_drivers()


#==================================
# Rocket's trajectory visualisation 
#==================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform


#==================================
# INPUTS
# t : time 
# T : thrust 
# r : position
# v : velocity in rocket's referential
# a : acceleration in rocket's referential
# phi, theta, psi : euler angles
#===================================

# ==============================
# vector equations

def vector_magnitude(vector):
    """
    compute magnitude of a vector
    param vector: vector with components of Cartesian form
    return magnitude: magnitude of vector
    """
    # NOTE: np.linalg.norm(v) computes Euclidean norm
    magnitude = 0
    for component in vector:
        magnitude += component ** 2
    return magnitude ** (1 / 2)

#==================================
# Create Dataframe
#==================================


# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
r = np.asarray(data['Traj.r'].tolist())
v = np.asarray(data['Rocket.Kin.v'].tolist())
a = np.asarray(data['Rocket.Dyn.a'].tolist())
r1 = np.asarray(data['Para.DynPar.r1'].tolist())
r2 = np.asarray(data['Para.DynPar.r2'].tolist())
euler = np.asarray(data['Rocket.Kin.Kin_ang'].tolist())
wind = np.asarray(data['Wind.v_wind.val'].tolist())
pres = np.asarray(data['Atmo.Pres.P'].tolist())


# find time i where the parachute appears 
time_parachute=0
while r1[time_parachute][0]==r2[time_parachute][0] and r1[time_parachute][1]==r2[time_parachute][1] and r1[time_parachute][2]==r2[time_parachute][2]:
    time_parachute+=1

r_then_r2 = []
for i in range(time_parachute):
    r_then_r2.append(r[i])
for i in range(time_parachute,len(r2)):
    r_then_r2.append(r2[i])


# # Raise an exception when the trajectory is not realistic and blame the creator of the rocket for the failure
# if r_then_r2[1][2] < 0:
#     raise Exception("Simulation fail: your rocket is maybe not realistic...")


r_then_r2 = np.array(r_then_r2)

# We calculate the mean of the maximum of the trajectory according to the 3 axis
K = (r_then_r2[:,0].max() + r_then_r2[:,1].max() +r_then_r2[:,2].max())/3 

ratio = K*l/50
#We then normalize the arrows on the plot
wind*=2*ratio
wind_b = []
for i in range(len(r_then_r2)):
    wind_b.append([-wind[i][0]/2,-wind[i][1]/2,r_then_r2[i][2]-wind[i][2]])

#On affiche le vecteur vent a l'origine du repère et à la hauteur où est la fusée (le vent ne dépend pas du temps)

rocket = np.array([2*l*ratio,0,0])
y = np.array([0,l*ratio,0])
z = np.array([0,0,l*ratio])

indy = []
indz = []
rock = []
for i in range(len(r)):
    rotation = R.from_euler('xyz', euler[i], degrees=False)
    vect1 = rotation.apply(rocket)
    vect2 = rotation.apply(y)
    vect3 = rotation.apply(z)
    norm_v1 = vector_magnitude(vect1)
    norm_v2 = vector_magnitude(vect2)
    norm_v2 = vector_magnitude(vect3)
    for b in vect1:
        b = b/norm_v1
    for c in vect2:
        c = c/norm_v2
    for d in vect2:
        d = d/norm_v2
    rock.append(vect1)
    indy.append(vect2)
    indz.append(vect3)
    



rock = np.asarray(rock)
indy = np.asarray(indy)
indz = np.asarray(indz)


rt = rock



propagation_time_history = []
i = 0
for ti in time:
    iteration_results = {'t': ti, 
                         'rx': r[i][0], 'ry': r[i][1], 'rz': r[i][2],
                         'r1x': r1[i][0], 'r1y': r1[i][1], 'r1z': r1[i][2],
                         'r2x': r2[i][0], 'r2y': r2[i][1], 'r2z': r2[i][2],
                         'r_then_r2_x': r_then_r2[i][0], 'r_then_r2_y': r_then_r2[i][1], 'r_then_r2_z': r_then_r2[i][2],
                         'vx': v[i][0], 'vy': v[i][1], 'vz': v[i][2],
                         'ax': a[i][0], 'ay': a[i][1], 'az': a[i][2],
                         'rtx': rt[i][0], 'rty': rt[i][1], 'rtz': rt[i][2],
                         'indyx': indy[i][0], 'indyy': indy[i][1], 'indyz': indy[i][2],
                         'indzx': indz[i][0], 'indzy': indz[i][1], 'indzz': indz[i][2],
                         'wind_bx':wind_b[i][0], 'wind_by':wind_b[i][1], 'wind_bz':wind_b[i][2],
                         'windx':wind[i][0], 'windy':wind[i][1], 'windz':wind[i][2],
                        }
    i+=1
    propagation_time_history.append(iteration_results)




df = pd.DataFrame(propagation_time_history)

#==================================
# Visualise trajectory
#==================================

# Arrow3D used for drawing arrow as vectors in 3D space
class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)
        
    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs) 


def vector_arrow_3d(x0, x1, y0, y1, z0, z1, color):
    """
    method to create a new arrow in 3d for vectors
    return Arrow3D: new vector
    """
    return Arrow3D(x0, x1, y0, y1, z0, z1,
                   mutation_scale=10, lw=1,
                   arrowstyle='-|>', color=color)


class Animator:

    def __init__(self, simulation_results):
        self.simulation_results = simulation_results
        self.vector_lines = []
        # =======================================
        #  configure plots and data structures

        self.fig = plt.figure(figsize=(15, 8))
        self.fig.subplots_adjust(left=0.05,
                                 bottom=None,
                                 right=0.95,
                                 top=None,
                                 wspace=None,
                                 hspace=0.28)


        self.ax1 = self.fig.add_subplot(projection='3d')
        # self.ax2 = self.fig.add_subplot()

        self.set_axes_limits()

        # axis 1 - 3D visualisation

        self.trajectory, = self.ax1.plot([], [], [], 'bo', markersize=1)


    def draw_xyz_axis(self, x_lims, y_lims, z_lims):
        """
        draw xyz axis on ax1 3d plot
        param x_lims: upper and lower x limits
        param y_lims: upper and lower y limits
        param z_lims: upper and lower z limits
        """
        self.ax1.plot([0, 0], [0, 0], [0, 0], 'ko', label='Origin')
        self.ax1.plot(x_lims, [0, 0], [0, 0], 'k-', lw=1)
        self.ax1.plot([0, 0], y_lims, [0, 0], 'k-', lw=1)
        self.ax1.plot([0, 0], [0, 0], z_lims, 'k-', lw=1)
        self.text_artist_3d('x', 'k', x_lims[1], 0, 0)
        self.text_artist_3d('y', 'k', 0, y_lims[1], 0)
        self.text_artist_3d('z', 'k', 0, 0, z_lims[1])
        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('y')
        self.ax1.set_zlabel('z')

    def text_artist_3d(self, text, color, x=0, y=0, z=0):
        """
        create new text artist for the plot
        param txt: text string
        param color: text color
        param x: x coordinate of text
        param y: y coordinate of text
        param z: z coordinate of text
        """
        return self.ax1.text(x, y, z, text, size=11, color=color)

    def set_axes_limits(self):
        """
        set the axis limits for each plot, label axes
        """
        lim_params = ['r1']
        x_lims = self.get_limits(lim_params, 'x')
        y_lims = self.get_limits(lim_params, 'y')
        z_lims = self.get_limits(lim_params, 'z')

        self.ax1.set_xlim3d(x_lims)
        self.ax1.set_ylim3d(y_lims)
        self.ax1.set_zlim3d(z_lims)
        self.draw_xyz_axis(x_lims, y_lims, z_lims)




    def get_limits(self, params, axis):
        """
        get upper and lower limits for parameter
        param axis: get limits for axis, i.e x or y
        param params: list of varaible names
        """
        lower_lim, upper_lim = 0, 0
        for p in params:
            m = max(self.simulation_results['%s%s' % (p, axis)])
            if m > upper_lim:
                upper_lim = m
            m = min(self.simulation_results['%s%s' % (p, axis)])
            if m < lower_lim:
                lower_lim = m
            m = max(abs(lower_lim - 0.05), upper_lim + 0.05)
        return lower_lim - 0.05,upper_lim + 0.05

    def config_plots(self):
        """
        Setting the axes properties such as title, limits, labels
        """
        self.ax1.set_title('Trajectory Visualisation')
        self.ax1.set_position([0.25, 0, 0.5, 1])
        self.ax1.set_aspect('equal')

    def visualize(self, i):

        # ######
        # axis 1
        row = self.simulation_results.iloc[i]

        if i<time_parachute:

            # define vectors
            vectors = [vector_arrow_3d(0, 0, 0, row.rx, row.ry, row.rz, 'g'), 
                    vector_arrow_3d(row.rx, row.ry, row.rz, row.rtx, row.rty, row.rtz, 'r'),
                    vector_arrow_3d(row.rx, row.ry, row.rz, row.indyx, row.indyy, row.indyz, 'k'),
                    vector_arrow_3d(row.rx, row.ry, row.rz, row.indzx, row.indzy, row.indzz, 'k'),
                    vector_arrow_3d(row.wind_bx, row.wind_by, row.wind_bz, row.windx, row.windy, row.windz, 'b'),
                    ]

        else:
            vectors = [vector_arrow_3d(0, 0, 0, row.r2x, row.r2y, row.r2z, 'g'), 
                    #    vector_arrow_3d(0, 0, 0, row.r1x, row.r1y, row.r1z, 'r'), 
                    vector_arrow_3d(row.r2x, row.r2y, row.r2z, (row.r1x-row.r2x)*ratio, (row.r1y-row.r2y)*ratio*5, (row.r1z-row.r2z)*ratio*5, 'r'),
                    vector_arrow_3d(row.wind_bx, row.wind_by, row.wind_bz, row.windx, row.windy, row.windz, 'b'),
                    ]

        # add vectors to figure
        [self.ax1.add_artist(vector) for vector in vectors]

        # remove previous vectors from figure
        if self.vector_lines:
            [vector.remove() for vector in self.vector_lines]
        self.vector_lines = vectors

        # update trajectory for current time step
        self.trajectory.set_data(self.simulation_results['r_then_r2_x'][:i], self.simulation_results['r_then_r2_y'][:i])
        self.trajectory.set_3d_properties(self.simulation_results['r_then_r2_z'][:i])


        # plt.pause(0.05)

    def animate(self):
        """
        animate drawing velocity vector as particle
        moves along trajectory
        return: animation
        """
        return animation.FuncAnimation(self.fig,
                                       self.visualize,
                                       frames=len(time),
                                       init_func=self.config_plots(),
                                       blit=False,
                                       repeat=True,
                                       interval=5)


# =======================================
# trajectory animation

animator = Animator(simulation_results=df)
anim = animator.animate()
# anim.save('rocket_traj.gif') # If you want to save the animation as a gif or mp4 etc.
plt.show()


# =======================================
# Flight Data

print('\n')
print("Apogee Height: ", np.max(np.array(r_then_r2)[:,2]), "m")
print('\n')
#print("Horizontal Position at Apogee: ", np.min(r2[:,0]), 'm')
#print('\n')
print("Total Flight Time: ", time[-1], "s")
print('\n')
print("Landing Point: ", np.array(r_then_r2)[-1,0], "m")
print('\n')
print("Lowest Pressure", np.min(pres))
print('\n')


def simulation_2d_plots():
    '''
    Plot various 2d plots
    '''
    if IPython.get_ipython() is not None:
        IPython.get_ipython().run_line_magic('matplotlib', 'inline')

    global time, pres, r_then_r2
    plt.plot(time, np.array(r_then_r2)[:,2])
    plt.title("Rocket Altitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.show()

    plt.plot(np.array(r_then_r2)[:,0], np.array(r_then_r2)[:,2])
    plt.title("Rocket XZ Trajectory")
    plt.xlabel("Horizontal Displacement (m)")
    plt.ylabel("Height (m)")
    plt.show()

    plt.plot(time, pres)
    plt.title("Pressure over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Pressure (Pa)")
    plt.show()


if IPython.get_ipython() is None:
    simulation_2d_plots()