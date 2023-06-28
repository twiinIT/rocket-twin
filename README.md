# rocket-twin - PSC - X rocket

rocket-twin is a 6 degree of freedom digital-twin of a rocket. You can create a rocket interactively through a jupyter notebook, visualize it and plot its flight trajectory.

This library was built with CoSApp, an open source framework allowing complex systems simulation. You can read more about it [here](https://cosapp.readthedocs.io/en/latest/).

## Getting Started

After cloning the repository thanks to
```bash
git clone https://github.com/twiinIT/rocket-twin.git
```

install the dependencies via

```bash
pip install -r requirements.txt
```

## How to use

In order to use the graphic interface, move to the UI directory
and browse the jupyter notebook `user_interface.ipynb`.

## Overview

Create your own rocket using `user_interface.ipynb` by specifying its geometric and mass properties in widgets.

<img title="Specify geometric and mass properties" alt="Screen shot of the user interface" src="./media/geometry_widget.png" width="700">

Chose the right motor for your rocket from a large database using a simple browser widget.

<img title="Select the impulse class" alt="Screen shot of the user interface" src="./media/motor_widget1.png" width="700">

<img title="Select the diameter of the rocket" alt="Screen shot of the user interface" src="./media/motor_widget2.png" width="700">

<img title="Select your desired motor" alt="Screen shot of the user interface" src="./media/motor_widget3.png" width="700">

Chose the flight parameters for a more realistic simulation.

The project provides a random wind profile generator to test your rocket's stability.

<img title="Flight parameters widget" alt="Screen shot of the user interface" src="./media/launch_parameters.png" width="500" >


When everything is specified, visualise the 3D model of your rocket to verify if the geometry matches your design.

<img title="Plot your rocket's 3D model" alt="Screen shot of rocket 3D model example" src="./media/rocket_model.png" width="700">

You're now ready to go for a simulation !

<img title="Rocket simulated trajectory" alt="Gif of a simulation" src="./media/rocket_traj.gif" width="700">


## Contributing

Please contact TwiinIT if you want to contribute to this project.
