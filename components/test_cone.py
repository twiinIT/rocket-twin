from create_mesh import create_mesh
from inertia import cog, inertia_moments
from nose_cone import NoseCone
from cosapp.drivers import RunOnce
import numpy as np

R = 3
H = 3
dens = 300
npts = 3

def f(x, y, z):

    return x**2 + y**2 - (z - H)**2

cone1 = NoseCone('cone1')
cone1.Rc = R
cone1.Lc = H
cone1.rho = dens

cone1.add_driver(RunOnce('run'))
cone1.run_drivers()

print(cone1.I)

xx, yy, zz = create_mesh(f, -R, R, -R, R, 0, H, npts, npts, npts)

x = xx.flatten()
y = yy.flatten()
z = zz.flatten()

xg, yg, zg = cog(x, y, z)

Ix, Iy, Iz = inertia_moments(x, y, z, xg, yg, zg, dens)

print([Ix, Iy, Iz])



