import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

def create_mesh(f, x0, xf, y0, yf, z0, zf, nx, ny, nz, hollow=False, plot=True):

    x = np.linspace(x0, xf, nx)
    y = np.linspace(y0, yf, ny)
    z = np.linspace(z0, zf, nz)

    xx, yy, zz = np.meshgrid(x, y, z)

    index = np.where(f(xx, yy, zz) > 0)
    zz[index] = np.nan

    if plot:
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(xx, yy, zz)
        plt.show()

    return xx, yy, zz

def create_mesh2(H, R, n, hollow=False, plot=True):

    cone = pv.Cone(center=(0,0,0), direction=(0,0,1), height=H, radius=R, resolution=n)

    if plot:
        cone.plot(show_grid = True)

    return cone



