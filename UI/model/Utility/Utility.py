import os

import pandas as pd

current_path = os.getcwd()
assert current_path.endswith(
    "UI"
), f"Move to rocket-twin\\UI in order to run the model. You are now at {current_path}"

thrust_data = pd.read_csv("model/Utility/thrust.txt", header=None)
times = list(thrust_data.iloc[0])
thrusts = list(thrust_data.iloc[1])


def mean(x, y, fx, fy, t):
    """Calculates the linear regression between x and y and evaluates it at t"""
    percent = (t - x) / (y - x)
    return fx + (fy - fx) * percent


def thrust(time):
    """Calculates the thrust of the rocket"""

    # If the time is superior to the last data point there is no more thrust
    if time >= times[-1]:
        return 0

    i = 0
    while times[i] <= time:
        i += 1

    return mean(times[i - 1], times[i], thrusts[i - 1], thrusts[i], time)
