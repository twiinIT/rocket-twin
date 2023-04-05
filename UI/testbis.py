import pyvista as pv
import numpy as np

import include.init_rocket.mesh_creation as mc
import test as test

cylinder = test.nose(shape_function = 'ellipse', OVpnum=4,Cpnum=4)

my_mesh = cylinder.stl_mesh

print(my_mesh.get_mass_properties())

my_mesh.save('cylinder.stl')

mesh = pv.read('cylinder.stl')

# Compute normals
mesh.compute_normals(cell_normals=True, point_normals=False, inplace=True)

mesh.plot_normals(mag=0.2, faces=True)



# # Get list of cell IDs that meet condition
# ids = np.arange(mesh.n_cells)[mesh['Normals'][:, 0] < 0.0]

# # Extract those cells
# top = mesh.extract_cells(ids)

# top.plot(jupyter_backend='pythreejs')