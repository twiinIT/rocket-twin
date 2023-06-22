from create_mesh import create_mesh
from inertia import cog, volume
from nose_parabolic import NoseParabolic
from cosapp.drivers import RunOnce
import numpy as np

def test_parabolic(R, H, dens, npts):

    ## Analytical paraboloid

    par_an = NoseParabolic('par_an')
    par_an.Lp = R
    par_an.Rp = H
    par_an.rho = dens

    par_an.add_driver(RunOnce('run'))
    par_an.run_drivers()

    ## Paraboloid created with numpy mesh

    # Paraboloid function for mesh creation

    def f(x, y, z):

        return x**2 + y**2 - (R**2/H)*(H - z)
    
    # Paraboloid function for volume integration

    def fv(x, y):

        return H - (x**2 + y**2)/(R**2/H)
    
    # Paraboloid mesh

    xx, yy, zz = create_mesh(f, -R, R, -R, R, 0, H, npts, npts, npts, plot=True)

    x = xx.flatten()
    y = yy.flatten()
    z = zz.flatten()

    # Paraboloid center of gravity

    xg, yg, zg = cog(x, y, z)

    # Paraboloid volume

    V = volume(fv, R)

    # Paraboloid mass

    m = dens*V

    ## Outputs Comparison

    print('\n')
    print("Analytical volume: ", par_an.m/dens)
    print("Numpy mesh volume: ", V)

    print('\n')
    print("Analytical CoG: ", H - par_an.Xcg)
    print("Numpy mesh CoG: ", zg)

test_parabolic(3, 3, 300, 20)
