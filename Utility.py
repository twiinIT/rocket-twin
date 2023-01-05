import pandas as pd

thrust_data = pd.read_csv("thrust.txt", header=None)
times = list(thrust_data.iloc[0])
thrusts = list(thrust_data.iloc[1])

aero_data = pd.read_csv("aero.txt", header=None)
attack = list(aero_data.iloc[:, 0])
Cx_list = list(aero_data.iloc[:, 2])
Cn_list = list(aero_data.iloc[:, 1])
Z_CPA_list = list(aero_data.iloc[:, 3])

def mean(x, y, fx, fy, t):
    """Calculates the linear regression between x and y and evaluates it at t"""
    percent = (t - x)/(y - x)
    return (fx + (fy - fx)*percent)


def thrust(time):
    """Calculates the thrust of the rocket"""

    #If the time is superior to the last data point there is no more thrust
    if time >= times[-1]:
        return 0

    i=0
    while times[i] <= time:
        i += 1

    return mean(times[i - 1], times[i], thrusts[i - 1], thrusts[i], time) 


def aeroCoefs(incidence):
    """Returns a tuple Cx, Cn, Z_CPA of the aerodynamic coefficients"""        
    i = 0
    if (incidence > attack[-1]):
        i = len(attack) - 1
    else:
        while attack[i] <= incidence:
            i += 1

    Cn = mean(attack[i - 1], attack[i], Cn_list[i - 1], Cn_list[i], incidence)

    Cx = mean(attack[i - 1], attack[i], Cx_list[i - 1], Cx_list[i], incidence)

    Z_CPA = mean(attack[i - 1], attack[i], Z_CPA_list[i - 1], Z_CPA_list[i], incidence)

    return Cx, Cn, Z_CPA