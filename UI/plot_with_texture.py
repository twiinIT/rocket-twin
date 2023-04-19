import json



from include.init_rocket.RocketPlotter import RocketPlotter
from include.init_rocket.CustomRocket import CustomRocket

# plot the rocket using pyvista 

def main():
    with open("./include/init_rocket/rocket_dict.json", "r") as f:
        my_rocket = json.load(f)
    
    rocket = CustomRocket.fromDict(my_rocket)
    plotter = RocketPlotter(rocket)

    plotter.plot(opened = True, only_ext = False, render = 'textures', )

if __name__ == "__main__":
    main()