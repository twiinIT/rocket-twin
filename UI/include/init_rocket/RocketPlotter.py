import pyvista as pv
import include.init_rocket.CustomRocket
import include.init_rocket.mesh.Solid

class RocketPlotter():
    '''
    Class for rocket plotting using pyvista.

    Attributes:
        rocket (CustomRocket): The rocket to be plot.
    '''
    def __init__(self, rocket):
        self.rocket = rocket
    
    
    def plot(self, only_ext=False, opened=True):
        '''
        Plot the rocket using pyvista.
        '''
        unavailable_textures = ['delrin','acrylique','depron_xps','kraft_phenolique','tube_quantum','custom']

        plotter = pv.Plotter()

        components = self.rocket.asList(only_ext)

        for component, texture_name in zip(components, self.rocket.textures):
            mesh = component.to_vista_mesh(opened)

            if texture_name in unavailable_textures:
                tex = None
            else:
                file_name = "./include/init_rocket/textures/"+texture_name+".jpg"
                tex = pv.read_texture(file_name)
            plotter.add_mesh(mesh, show_edges=False, texture = tex, metallic=0.8)

        plotter.add_axes(interactive=True)
        plotter.show(jupyter_backend = 'pythreejs')