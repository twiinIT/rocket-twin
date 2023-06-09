import numpy as np
import scipy as sp

def cog(x, y, z):

    xg = 0
    yg = 0
    zg = 0
    L = 0

    for i in range(len(x)):
        if np.isnan(z[i]) == False:
            xg += x[i]
            yg += y[i]
            zg += z[i]
            L += 1

    xg = xg/L
    yg = yg/L
    zg = zg/L

    return xg, yg, zg

def inertia_moments(x, y, z, xg, yg, zg, m):

    Ix = 0
    Iy = 0
    Iz = 0
    L = 0

    for i in range(len(x)):
        if np.isnan(z[i]) == False:
            Ix += (y[i] - yg)**2 + (z[i] - zg)**2
            Iy += (x[i] - xg)**2 + (z[i] - zg)**2
            Iz += (x[i] - xg)**2 + (y[i] - yg)**2
            L += 1

    Ix *= m/L
    Iy *= m/L
    Iz *= m/L

    return Ix, Iy, Iz

def volume(f, R):

    def func(z, y, x):

        return 1

    def gfun(x):

        return -np.sqrt(R**2 - x**2)
    
    def hfun(x):

        return np.sqrt(R**2 - x**2)
    
    def qfun(x, y):

        return 0
    
    def rfun(x, y):

        return f(x, y)
    
    V = sp.integrate.tplquad(func, -R, R, gfun, hfun, qfun, rfun)

    return V[0]