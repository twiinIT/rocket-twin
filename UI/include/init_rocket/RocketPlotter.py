import include.init_rocket.CustomRocket
import include.init_rocket.mesh.Solid
import pyvista as pv


class RocketPlotter:
    """
    Class for rocket plotting using pyvista.

    Attributes:
        rocket (CustomRocket): The rocket to be plot.
    """

    tex_to_color = {
        "custom": [1.0, 1.0, 1.0],
        "motor": [1.0, 0.0, 0.0],
        "acier": [0.42363846997650634, 0.42363846997650634, 0.42363846997650634],
        "acrylique": [1.0, 1.0, 1.0],
        "aluminium": [0.42363846997650634, 0.42363846997650634, 0.42363846997650634],
        "balsa": [0.9651576453696336, 0.8906137434740409, 0.7792442660481324],
        "blue_tube": [0.4101794593311916, 0.6919089697721963, 0.8513988390771028],
        "bouleau": [1.0, 1.0, 1.0],
        "carton": [0.8363084242078993, 0.6959518602159288, 0.5049607340494792],
        "contre_plaque": [0.9208919704861112, 0.7991272786458333, 0.6233024088541667],
        "delrin": [1.0, 1.0, 1.0],
        "depron_xps": [1.0, 1.0, 1.0],
        "erable": [0.8507417442908654, 0.6888096604567308, 0.5356387845552885],
        "fibre_carbon": [0.1, 0.1, 0.1],
        "fibre_verre": [0.7810631618885147, 0.7810631618885147, 0.7810631618885147],
        "kraft_phenolique": [1.0, 1.0, 1.0],
        "laiton": [0.6976380582966433, 0.5649386481637912, 0.3063599501484667],
        "liege": [0.8387979023893546, 0.6273034084385187, 0.410780851038204],
        "blue_xps": [0.4101794593311916, 0.6919089697721963, 0.8513988390771028],
        "nylon": [1.0, 1.0, 1.0],
        "papier": [0.8975090544577118, 0.8975090544577118, 0.8975090544577118],
        "pin": [0.87272848304643, 0.7704099893841538, 0.6521671185287836],
        "polycarbonate": [0.8297203414351851, 0.8461838188014403, 0.8803575049296982],
        "polystyrene": [0.9015991439962476, 0.9009592665337711, 0.9117466544031426],
        "polystyrene_eps": [0.9015991439962476, 0.9009592665337711, 0.9117466544031426],
        "pvc": [0.8647425889756944, 0.8644301323784722, 0.8721728515625],
        "sapin": [0.9745615981533545, 0.8695536741427576, 0.7064131077139802],
        "tilleul": [0.9645160953177258, 0.868472280286139, 0.6758425945280565],
        "titane": [0.5934933710377734, 0.5934933710377734, 0.5934933710377734],
        "tube_quantum": [1.0, 1.0, 1.0],
    }

    def __init__(self, rocket):
        self.rocket = rocket

    def plot(self, only_ext=False, opened=True, render="colors"):
        """
        Plot the rocket using pyvista.
        The 'textures' render is not available on jupyter notebooks.
        """
        available_render = ["colors", "textures"]
        assert (
            render in available_render
        ), f"Unavailable backend. Valid options are: {', '.join(available_render)}"

        unavailable_textures = [
            "delrin",
            "bouleau",
            "acrylique",
            "depron_xps",
            "kraft_phenolique",
            "tube_quantum",
            "custom",
        ]

        plotter = pv.Plotter(notebook=True)

        # Plot the cog and cpa as spheres
        if opened:
            cog = self.rocket.get_mass_properties()[2]
            plotter.add_mesh(pv.Sphere(0.01, cog), color="r")
            cpa = self.rocket.get_cpa()
            plotter.add_mesh(pv.Sphere(0.01, cpa), color="g")

        components = self.rocket.asList(only_ext)

        for component, texture_name in zip(components, self.rocket.textures):
            mesh = component.to_vista_mesh(opened)
            if render == "textures":
                color = None
                if texture_name in unavailable_textures:
                    tex = None
                else:
                    file_name = (
                        "./include/init_rocket/textures/" + texture_name + ".jpg"
                    )
                    tex = pv.read_texture(file_name)
            else:
                tex = None
                color = self.tex_to_color[texture_name]

            plotter.add_mesh(
                mesh, show_edges=False, texture=tex, color=color, metallic=0.8
            )

        plotter.add_axes(interactive=True)
        plotter.show(jupyter_backend="pythreejs")


# Code to calculate the average color of an image
# Used to create the tex_to_color dict


# from PIL import Image
# import numpy as np

# textures = {"Customized":"custom",
#              "Acier": "acier",
#              "Acrylique": "acrylique",
#              "Aluminium": "aluminium",
#              "Balsa": "balsa",
#              "Blue tube": "blue_tube",
#              "Bouleau": "bouleau",
#              "Carton": "carton",
#              "Contre-plaqué (bouleau)": "contre_plaque",
#              "Delrin": "delrin",
#              "Depron (XPS)": "depron_xps",
#              "Erable": "erable",
#              "Fibre de carbone": "fibre_carbon",
#              "Fibre de verre": "fibre_verre",
#              "Kraft phénolique": "kraft_phenolique",
#              "Laiton": "laiton",
#              "Liège": "liege",
#              "Mousse Bleue de polystyrène (XPS)": "blue_xps",
#              "Nylon": "nylon",
#              "Papier (bureau)": "papier",
#              "Pin": "pin",
#              "Polycarbonate (Lexan)": "polycarbonate",
#              "Polystyrène": "polystyrene",
#              "Polystyrène (générique EPS)": "polystyrene_eps",
#              "PVC": "pvc",
#              "Sapin": "sapin",
#              "Tilleul": "tilleul",
#              "Titane": "titane",
#              "Tube Quantum": "tube_quantum"}

# tex_to_color = {}

# for key,value in textures.items():
#     unavailable_textures = ['delrin','bouleau','acrylique','depron_xps','kraft_phenolique','tube_quantum','custom','fibre_carbon','nylon']
#     if value in unavailable_textures:
#         res = [1.,1.,1.]
#     else:
#         img = Image.open("include/init_rocket/textures/"+value+".jpg")
#         img = np.asarray(img)

#         res = np.mean(img,axis=(0,1))

#         res = res/256

#     tex_to_color[value] = list(res)

# tex_to_color
