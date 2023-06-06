import json

import matplotlib.pyplot as plt
import numpy as np
from cosapp.base import System
from Ports import VelPort
from scipy.interpolate import interp1d


class Wind(System):
    def setup(self):
        self.add_output(VelPort, "v_wind")
        self.add_inward(
            "r", np.zeros(3), desc="rocket position in earth referential", unit="m"
        )
        self.add_inward(
            "r1",
            np.zeros(3),
            desc="rocket position in earth referential after parachute deployment",
            unit="m",
        )

        # Parachute
        self.add_inward("ParaDep", False, desc="Parachute Deployed", unit="")

        self.add_inward("wind_on", True, desc="Is the wind on ?", unit="")

    def compute(self):
        if not self.wind_on:
            self.v_wind.val = [0.0, 0.0, 0.0]
            return

        if self.ParaDep:
            self.v_wind.val = get_wind(self.parent.Para.DynPar.r1[2])
        else:
            self.v_wind.val = get_wind(self.r[2])


with open("./include/init_rocket/rocket_dict.json", "r") as f:
    rocket_dict = json.load(f)
    average_speed = rocket_dict["wind_average_speed"]


def wind(average_speed):
    # Define the number of altitude steps and the maximum height
    n_steps_dir = 10  # number of steps for wind direction
    n_steps_spd = 10  # number of steps for wind speed
    max_height = 5000  # in meters

    # Generate random wind directions and speeds for each altitude step
    wind_initial_direction = np.random.uniform(low=0, high=360, size=1)  # in degrees
    wind_directions = np.abs(
        np.random.normal(loc=wind_initial_direction, scale=20, size=n_steps_dir)
    )  # in degrees
    wind_speeds = np.abs(np.random.normal(loc=average_speed, scale=1, size=n_steps_spd))
    wind_speeds = np.insert(wind_speeds, 0, 0)  # couche limite au sol
    # print(wind_speeds)

    # Create a cubic spline interpolation of wind direction and speed
    altitudes_dir = np.linspace(0, max_height, n_steps_dir)  # in meters
    altitudes_spd = np.linspace(0, max_height, n_steps_spd + 1)  # in meters
    altitudes_spd[1] = 100  # fin de la couche limite à 50 mètres de haut
    interp_directions = interp1d(altitudes_dir, wind_directions, kind="cubic")
    interp_speeds = interp1d(altitudes_spd, wind_speeds, kind="linear")

    # Create a plot of the wind direction profile
    # fig1, ax1 = plt.subplots()
    altitudes_plot_dir = np.linspace(0, max_height, 500)  # in meters
    directions_plot = interp_directions(altitudes_plot_dir) % 360  # in degrees
    # ax1.plot(directions_plot, altitudes_plot_dir)
    # ax1.set_xlim([0, 360])
    # ax1.set_ylim([0, max_height])
    # ax1.set_xlabel('Wind direction (degrees)')
    # ax1.set_ylabel('Altitude (m)')
    # ax1.set_title('Random wind direction profile')

    # Create a plot of the wind speed profile
    # fig2, ax2 = plt.subplots()
    altitudes_plot_spd = np.linspace(0, max_height, 500)  # in meters
    speeds_plot = interp_speeds(altitudes_plot_spd)  # in meters per second
    # ax2.plot(speeds_plot, altitudes_plot_spd)
    # ax2.set_xlim([0, 30])
    # ax2.set_ylim([0, max_height])
    # ax2.set_xlabel('Wind speed (m/s)')
    # ax2.set_ylabel('Altitude (m)')
    # ax2.set_title('Random wind speed profile')
    # plt.show()
    sample = speeds_plot, directions_plot
    return sample


sample_wind = wind(average_speed)


def get_wind(alt):
    alt = int(alt // 10)  # on a un pas de 10 mètres pour cette fonction
    return [
        sample_wind[0][alt] * np.cos(sample_wind[1][alt] * np.pi / 180),
        sample_wind[0][alt] * np.sin(sample_wind[1][alt] * np.pi / 180),
        0,
    ]
