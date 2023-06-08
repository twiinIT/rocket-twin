import numpy as np
import matplotlib.pyplot as plt

def create_mesh(f, x0, xf, y0, yf, z0, zf, nx, ny, nz, hollow=False):

    x = np.linspace(x0, xf, nx)
    y = np.linspace(y0, yf, ny)
    z = np.linspace(z0, zf, nz)

    xx, yy, zz = np.meshgrid(x, y, z)
    rr2 = xx**2 + yy**2

    index = np.where(f(xx, yy, zz) > 0)
    print(index)
    zz[index] = None

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(xx, yy, zz)
    plt.show()

    return xx, yy, zz
