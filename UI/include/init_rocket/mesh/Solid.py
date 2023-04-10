import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import plotly.graph_objects as go
import pyvista as pv


class Solid:
    '''
    Class representing a solid object containing its mesh, and its mass properties (volume, mass, COG, matrix of inertia)

    Attributes:
        brute_mesh (BruteMesh): Object containing 'veritices'(numpy.array) and 'faces'(numpy.array) of the solid's mesh
        stl_mesh (stl.mesh): The corresponding stl.mesh object for the solid.
        plot_brute_mesh (BruteMesh): Object containing 'veritices'(numpy.array) and 'faces'(numpy.array) of the solid's to plot (may be different from the solid mesh)
        plot_stl_mesh (stl.mesh): The corresponding stl.mesh.
        density (float): The density of the Solid in kg/m^3. Equals 1e3 by default.
    '''


    class BruteMesh:
        '''
        Class used to store the brute mesh of the Solid.
        '''
        def __init__(self, vertices, faces) -> None:
            self.vertices = vertices
            self.faces = faces


    def __init__(self, brute_mesh : BruteMesh, stl_mesh : mesh.Mesh, plot_brute_mesh : BruteMesh, plot_stl_mesh : mesh.Mesh, density = 1e3) -> None:
        self.brute_mesh = brute_mesh
        self.stl_mesh = stl_mesh
        self.plot_brute_mesh = plot_brute_mesh
        self.plot_stl_mesh = plot_stl_mesh
        self.density = density


    @staticmethod
    def combine(solids):
        '''
        Combine Solid objects within the solids list.
        
        Returns:
            A Solid containing the combination of all solids with mean density of the combination.
        '''

        mean_density = 0
        n = len(solids)

        vertices, faces, vectors = solids[0].brute_mesh.vertices, solids[0].brute_mesh.faces, solids[0].stl_mesh.vectors
        pvertices, pfaces, pvectors = solids[0].plot_brute_mesh.vertices, solids[0].plot_brute_mesh.faces, solids[0].plot_stl_mesh.vectors

        for i in range(1,n):
            mean_density += solids[i].density

            v2,f2,vect2 = solids[i].brute_mesh.vertices, solids[i].brute_mesh.faces, solids[i].stl_mesh.vectors
            f2 = f2 + len(vertices)
            vertices = np.concatenate((vertices,v2))
            faces = np.concatenate((faces,f2))
            vectors = np.concatenate((vectors, vect2))

            pv2,pf2, pvect2 = solids[i].plot_brute_mesh.vertices, solids[i].plot_brute_mesh.faces, solids[i].plot_stl_mesh.vectors
            pf2 = pf2 + len(pvertices)
            pvertices = np.concatenate((pvertices,pv2))
            pfaces = np.concatenate((pfaces,pf2))
            pvectors = np.concatenate((pvectors, pvect2))

        brute_mesh = Solid.BruteMesh(vertices, faces)

        data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
        data['vectors'] = vectors
        stl_mesh = mesh.Mesh(data)
        
        plot_brute_mesh = Solid.BruteMesh(pvertices, pfaces)
        
        pdata = np.zeros(pfaces.shape[0], dtype=mesh.Mesh.dtype)
        pdata['vectors'] = pvectors
        plot_stl_mesh = mesh.Mesh(pdata)

        mean_density /= n

        return Solid(brute_mesh=brute_mesh, stl_mesh=stl_mesh, plot_brute_mesh=plot_brute_mesh, plot_stl_mesh=plot_stl_mesh, density = mean_density)
    

    def to_vista_mesh(self,opened=False):
        '''
        Create and return the pyvista mesh of the solid. opened=True for the opened mesh if available.
        '''
        if opened:
            vertices, faces = self.plot_brute_mesh.vertices, self.plot_brute_mesh.faces
        else:
            vertices, faces = self.brute_mesh.vertices, self.brute_mesh.faces
        faces = np.pad(faces,pad_width=((0,0),(1,0)), mode='constant', constant_values=3)

        mesh = pv.PolyData(vertices, faces)
        mesh.texture_map_to_plane(inplace=True)

        return mesh
    

    def show(self, method='mpl', opened = True):
        valid_methods = ['mpl', 'go']  # predefined list of valid strings
        assert method in valid_methods, f"Invalid shape function. Valid options are: {', '.join(valid_methods)}"

        if method == 'mpl':
            self.show_mpl(opened = opened)
        elif method == 'go':
            self.show_go(opened = opened)


    def show_mpl(self, opened = True):
        '''
        Plot the Solid using matplotlib.

        Args:
            all (bool): specifies if the whole solid (False) or its plotting part only (True). Set to False by default.
        '''
        pyplot.close()
        # Create a new plot
        figure = pyplot.figure()
        axes = figure.add_subplot(projection='3d')
        # Add mesh to the plot
        
        my_mesh = self.plot_stl_mesh if opened else self.stl_mesh

        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
        # Auto scale to the mesh size
        scale = my_mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)
        # Show the plot to the screen
        pyplot.show()
        
        return figure


    def show_go(self, opened = True):
        '''
        Plot the Solid using plotly.graph_objects.
        
        Args:
            opened (bool): specifies if the whole solid (False) or its plotting part only (True). Set to False by default.
        '''
        if opened:
            faces = self.plot_brute_mesh.faces
            vertices = self.plot_brute_mesh.vertices
        else:
            faces = self.brute_mesh.faces
            vertices = self.brute_mesh.vertices

        x,y,z = vertices.T
        i,j,k = faces.T

        figure = go.Figure(data=[go.Mesh3d(x=x,y=y,z=z,i=i,j=j,k=k,showscale=True)])

        # Set the aspect ratio of the 3D scene to match the data
        figure.update_layout(scene=dict(aspectmode="data"))

        figure.show()


    def get_inertia_wrt(self, point : np.ndarray):
        '''
        Get matrix of inertia with respect to the specified point [x,y,z] using the parallel axis theorem.
        '''
        volume, vmass, cog, inertia = self.stl_mesh.get_mass_properties_with_density(self.density)
        cog[cog<1e-10] = 0.
        inertia[inertia<1e-7] = 0.
        R = point - cog
        E = np.eye(3)

        inertia = inertia + vmass*( R.dot(R)*E - np.outer(R,R))

        return volume, vmass, inertia