import json

from include.init_rocket.custom_rocket import CustomRocket
from include.init_rocket.rocket_plotter import RocketPlotter

# plot the rocket using pyvista


def main():
    with open("./include/init_rocket/rocket_dict.json", "r") as f:
        my_rocket = json.load(f)

    rocket = CustomRocket.fromDict(my_rocket)
    plotter = RocketPlotter(rocket)

    plotter.plot(
        opened=True,
        only_ext=False,
        render="textures",
    )


if __name__ == "__main__":
    main()
