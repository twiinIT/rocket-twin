import numpy as np

def cog(x, y, z):

    xg = 0
    yg = 0
    zg = 0
    L = len(x)

    for i in range(L):
        if z[i] != np.nan:
            xg += x[i]
            yg += y[i]
            zg += z[i]

    xg = xg/L
    yg = yg/L
    zg = zg/L

    return xg, yg, zg

def inertia_moments(x, y, z, xg, yg, zg, rho):

    Ix = 0
    Iy = 0
    Iz = 0
    L = len(x)

    for i in range(L):
        if z[i] != np.nan:
            Ix += (y[i] - yg)**2 + (z[i] - zg)**2
            Iy += (x[i] - xg)**2 + (z[i] - zg)**2
            Iz += (x[i] - xg)**2 + (y[i] - yg)**2

    Ix *= rho
    Iy *= rho
    Iz *= rho

    return Ix, Iy, Iz
