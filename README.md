# Crazyflie AprilTag Tracking In Webots Simulator

This project shows using a Bitcraze Crazyflie drone in the Webots simulator 
to track and move towards AprilTag markers using OpenCV.
Originally, this project was supposed to be done on actual hardware, 
but after a series of technical issues, it was done in simulator instead ☹️.

## Quickstart
If you're just interested in running the project, see these Quickstart details. 
Otherwise, the rest of this README is dedicated to walking through the process of creating the project.
<details>

<summary>Quickstart</summary>

These instructions will get you up and running with this project quickly so you can see it working.
Read the rest of the README if you want to understand how it works.

Make sure you've installed
1. [Webots](https://www.cyberbotics.com/doc/guide/installation-procedure)
2. Python

Clone the project.
```shell
git clone https://github.com/BruceMcRooster/crazyflie-apriltag-tracking.git
cd crazyflie-apriltag-tracking
```

Next, install the Python dependencies for the project.
I recommend first creating a virtual environment, but you can do it without one.

<details>
<summary>Creating a Python virtual environment</summary>

First, create the virtual environment.
```shell
python3 -m venv ./.venv
```
Then activate it for your shell. 
All Python commands you execute will be run in this virtual environment,
keeping your global installation clean of dependencies.
Several different activation scripts will be created, so choose the one that's right for your shell.

**Bash/Zsh**
```shell
source ./.venv/bin/activate
```
**Fish**
```shell
source ./.venv/bin/activate.fish
```
Then continue the dependency installation with this activated.
If you ever need to close the terminal, reactivate by running the `source` command again.

To deactivate this virtual environment, run `deactivate`.
</details>

Run this to install all the dependencies you'll need.
```shell
pip install -r requirements.txt
```

Next, open Webots.

If you have not used Python in Webots before, you might need to set it up.
Follow [these](https://cyberbotics.com/doc/guide/using-python) instructions. 
If you created a virtual environment for the project in the previous step, 
you can point to the Python executable in the .venv folder from the settings window.

```/path/to/crazyflie-apriltag-tracking/.venv/bin/python```

Finally, open the world (`path/to/crazyflie-apriltag-tracking/worlds/world.wbt`) in Webots and hit run.
If you focus on the screen, you should be able to move the AprilTag.
Arrows keys move the AprilTag side to side, W and S move it up and down, and Q and E rotate it.
The drone should track this movement accordingly, or start looking for it if it loses tracking.

</details>
