from create_mesh import create_mesh, create_mesh2
from inertia import cog, inertia_moments, volume
from nose_cone import NoseCone
from cosapp.drivers import RunOnce
import numpy as np

def test_cone(R, H, dens, npts):

    ## Analytical cone

    cone_an = NoseCone('cone_an')
    cone_an.Rc = R
    cone_an.Lc = H
    cone_an.rho = dens

    cone_an.add_driver(RunOnce('run'))
    cone_an.run_drivers()

    ## Cone created with numpy mesh

    # Cone function for mesh creation

    def f(x, y, z):

        return x**2 + y**2 - (z - H)**2
    
    # Cone function for volume integration

    def fv(x, y):

        return H - np.sqrt(x**2 + y**2)/(R/H) 
    
    # Cone mesh
    xx, yy, zz = create_mesh(f, -R, R, -R, R, 0, H, npts, npts, npts, plot=True)
    
    x = xx.flatten()
    y = yy.flatten()
    z = zz.flatten()

    # Cone center of gravity
    xg, yg, zg = cog(x, y, z)

    # Cone volume
    V = volume(fv, R)

    # Cone mass
    m = dens*V

    # Cone principal inertia moments
    Ix, Iy, Iz = inertia_moments(x, y, z, xg, yg, zg, m)

    ##Cone volume calculated with pyvista

    # Cone pyvista mesh
    cone_pv = create_mesh2(H,R,npts)

    # Cone pyvista volume
    V_pv = cone_pv.volume

    ## Outputs Comparison

    print('\n')
    print("Analytical volume: ", cone_an.m/dens)
    print("Numpy mesh volume: ", V)
    print("Pyvista mesh volume: ", V_pv)

    print('\n')
    print("Analytical CoG: ", H - cone_an.Xcg)
    print("Numpy mesh CoG: ", zg)

    print('\n')
    print("Analytical inertia moments: ", cone_an.I)
    print("Numpy mesh inertia moments: ", np.array([Ix, Iy, Iz]))


test_cone(3, 3, 300, 100)