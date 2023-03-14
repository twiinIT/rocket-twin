from Earth import Earth
import numpy as np
from cosapp.drivers import RungeKutta, NonLinearSolver
from cosapp.recorders import DataFrameRecorder
from scipy.spatial.transform import Rotation as R


#Time-step
dt = 0.05

#Create System
earth = Earth('earth')

#Add RungeKutta driver
driver = earth.add_driver(RungeKutta(order=4, dt=dt))
driver.time_interval = (0, 40)

#Add NonLinearSolver driver
solver = driver.add_child(NonLinearSolver('solver', factor=1.0))


# Add a recorder to capture time evolution in a dataframe
driver.add_recorder(
    DataFrameRecorder(includes=['Traj.r', 'Rocket.Kin.v', 'Rocket.Kin.a', 'Rocket.Dyn.m', 'Rocket.Thrust.Fp', 'Rocket.Kin.Kin_ang', 'Rocket.Kin.av', 'Rocket.Aero.F', 'Traj.v.val', 'Wind.v_wind.val']),
    period=.1,
)

#Initial conditions and constants

l = 10 #Rocket's length on the plot

driver.set_scenario(
    init = {
        'Traj.r' : np.array([0., 0., l/2]),
        'Rocket.Kin.v' : np.array([0,0,0]),
        'Rocket.Kin.ar' : np.array([0, -np.pi/2, 0]),
        'Rocket.Kin.av' : np.zeros(3),
    },
    stop='Traj.v.val[2]<-1'

    )


earth.run_drivers()








#==================================
# Rocket's trajectory visualisation 
#==================================

import os
import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import animation
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
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

def vector_derivative(vector, wrt):
    """
    differentiate vector components wrt a symbolic variable
    param v: vector to differentiate
    param wrt: symbolic variable
    return V: velcoity vector and components in x, y, z
    """
    return [component.diff(wrt) for component in vector]


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


def unit_vector(from_vector_and_magnitude=None, from_othogonal_vectors=None, from_orthogonal_unit_vectors=None):
    """
    Calculate a unit vector using one of three input parameters.
    1. using vector and vector magnitude
    2. using orthogonal vectors
    3. using orthogonal unit vectors
    """

    if from_vector_and_magnitude is not None:
        vector_a, magnitude = from_vector_and_magnitude[0], from_vector_and_magnitude[1]
        return [component / magnitude for component in vector_a]

    if from_othogonal_vectors is not None:
        vector_a, vector_b = from_othogonal_vectors[0], from_othogonal_vectors[1]
        vector_normal = np.cross(vector_a, vector_b)
        return unit_vector(from_vector_and_magnitude=(vector_normal, vector_magnitude(vector_normal)))

    if from_orthogonal_unit_vectors is not None:
        u1, u2 = from_orthogonal_unit_vectors[0], from_orthogonal_unit_vectors[1]
        return np.cross(u1, u2)


def evaluate_vector(vector, time_step):
    """
    evaluate numerical vector components and magnitude @ti
    param numerical_vector: symbolic vector expression to evaluate @ti
    param ti: time step for evaluation
    return magnitude, numerical_vector: magnitude of vector and components evaluated @ti
    """
    numerical_vector = [float(component.subs(t, time_step).evalf()) for component in vector]
    magnitude = vector_magnitude(numerical_vector)
    return numerical_vector, magnitude


def direction_angles(vector, magnitude=None):
    """
    compute direction angles a vector makes with +x,y,z axes
    param vector: vector with x, y, z components
    param magnitude: magnitude of vector
    """
    magnitude = vector_magnitude(vector) if magnitude is None else magnitude
    return [sp.acos(component / magnitude) for component in vector]

# ==============================
# helper functions


def d2r(degrees):
    """
    convert from degrees to radians
    return: radians
    """
    return degrees * (np.pi / 180)


def r2d(radians):
    """
    convert from radians to degrees
    return: degrees
    """
    return radians * (180 / np.pi)



#==================================
# Create Dataframe
#==================================


# Retrieve recorded data
data = driver.recorder.export_data()
data = data.drop(['Section', 'Status', 'Error code'], axis=1)
time = np.asarray(data['time'])
r = np.asarray(data['Traj.r'].tolist())
v = np.asarray(data['Rocket.Kin.v'].tolist())
a = np.asarray(data['Rocket.Kin.a'].tolist())
euler = np.asarray(data['Rocket.Kin.Kin_ang'].tolist())
wind = np.asarray(data['Wind.v_wind.val'].tolist())
wind*=8 #on fait x10 pour l'affichage du vent sinon on verra rien
wind_b = []
#On affiche le vecteur vent a l'origine du repère et à la hauteur où est la fusée (le vent ne dépend pas du temps)


#Modélisation de l'axe de la fusée et de sa normale(grossie x5)
rocket = np.array([l*8,0,0])
y = np.array([0,l*5,0])
z = np.array([0,0,l*5])

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
    wind_b.append([-wind[i][0]/2,-wind[i][1]/2,r[i][2]-wind[i][2]])



rock = np.asarray(rock)
indy = np.asarray(indy)
indz = np.asarray(indz)


rt = rock


propagation_time_history = []


i = 0
for ti in time:
    iteration_results = {'t': ti, 
                         'rx': r[i][0], 'ry': r[i][1], 'rz': r[i][2],
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

print(df)

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
        lim_params = ['r']
        x_lims = self.get_limits(lim_params, 'x')
        y_lims = self.get_limits(lim_params, 'y')
        z_lims = self.get_limits(lim_params, 'z')

        self.ax1.set_xlim3d(x_lims)
        self.ax1.set_ylim3d(y_lims)
        self.ax1.set_zlim3d(z_lims)
        self.draw_xyz_axis(x_lims, y_lims, z_lims)

        t_lims = self.get_limits(['t'], '')



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

        # define vectors
        vectors = [vector_arrow_3d(0, 0, 0, row.rx, row.ry, row.rz, 'g'), 
                   vector_arrow_3d(row.rx, row.ry, row.rz, row.rtx, row.rty, row.rtz, 'r'),
                   vector_arrow_3d(row.rx, row.ry, row.rz, row.indyx, row.indyy, row.indyz, 'k'),
                   vector_arrow_3d(row.rx, row.ry, row.rz, row.indzx, row.indzy, row.indzz, 'k'),
                vector_arrow_3d(row.wind_bx, row.wind_by, row.wind_bz, row.windx, row.windy, row.windz, 'b'),
                  ]

        # add vectors to figure
        [self.ax1.add_artist(vector) for vector in vectors]

        # remove previous vectors from figure
        if self.vector_lines:
            [vector.remove() for vector in self.vector_lines]
        self.vector_lines = vectors


        # update trajectory for current time step
        self.trajectory.set_data(self.simulation_results['rx'][:i], self.simulation_results['ry'][:i])
        self.trajectory.set_3d_properties(self.simulation_results['rz'][:i])


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
plt.show()

