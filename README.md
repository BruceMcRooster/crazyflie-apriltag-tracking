# Crazyflie AprilTag Tracking In Webots Simulator

This project shows using a Bitcraze Crazyflie drone in the Webots simulator 
to track and move towards AprilTag markers using OpenCV.
Originally, this project was supposed to be done on actual hardware, 
but after a series of technical issues, it was done in simulator instead ☹️.

## Quickstart
If you're just interested in running the project, see these Quickstart details. 
Otherwise, the rest of this README is dedicated to walking through the process of creating the project.
<details><summary>Quickstart</summary>
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

<details><summary>Creating a Python virtual environment</summary>
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

## Setup
Before you get started on making your own Crazyflie drone track AprilTags, you'll need to do some setup.

### Install Tools
First, make sure you've installed Python (version 3.8 or higher) and [Webots](https://www.cyberbotics.com/doc/guide/installation-procedure),
which is the simulator we'll be using.

### Create A Project
Create a folder for this project.

Next, we'll create a basic Webots project.
Create 2 folders in your project file: `controllers` and `worlds`.

Inside `worlds`, create a file called `world.wbt`, and paste the contents of 
[this](https://github.com/BruceMcRooster/crazyflie-apriltag-tracking/blob/241355c74062701479ea734ecbaa26e922c0252f/worlds/world.wbt)
file into it.

Inside `controllers`, create a folder called `drone_controller`.
Inside that, create two files: `drone_controller.py` and `pid_controller.py`.
Copy [this](https://github.com/BruceMcRooster/crazyflie-apriltag-tracking/blob/241355c74062701479ea734ecbaa26e922c0252f/controllers/drone_controller/drone_controller.py)
code into `drone_controller.py` and [this](https://github.com/BruceMcRooster/crazyflie-apriltag-tracking/blob/241355c74062701479ea734ecbaa26e922c0252f/controllers/drone_controller/pid_controller.py)
code into `pid_controller.py`.

These three files are a combination of example code included in Webots by Bitcraze, the makers of the Crazyflie drone.
You can find the two starter projects they were drawn from in the "File > Open Sample World..." menu in Webots,
under "robots > bitcraze > crazyflie". 
The Python code is a modification of the code from the `crazyflie_apartment.wbt` project,
and the world file is a modification of the code from the `crazyflie.wbt` project.

If you open the Webots simulator and open the `world.wbt` file you created, you should see this.
![A drone on a red and white wood checkerboard floor, with a black square in the top left corner](Pictures/new_world.png)

You'll also probably see an error in the console window. That's where the next part comes in.

### Install Dependencies
The Python script you just created depends on a library. 
We need to install that library to be able to use it.

For this project, I recommend creating a virtual environment, 
which will keep all the dependencies we need separate from the rest of your Python installation.
You don't need one, but I highly recommend creating one. 
You can skip the next section if you don't want one.

#### Create A Python Virtual Environment
Open your project folder[^1] in a terminal and run the following command.
```shell
python3 -m venv ./.venv
```
This will create a new virtual Python environment. 
To activate it in your terminal so you can install things, run this if you use Bash or Zsh
```shell
source ./.venv/bin/activate
```
or this if you use Fish Shell
```shell
source ./.venv/bin/activate.fish
```
If you don't know which one you use, run the first command; it'll probably be the right one. 
If you use another shell, the `.venv/bin` folder contains several other activation scripts for various shells.
You can probably find the one you need.

Whenever you want to work on this project in the terminal, you'll want to run that `source` command again.
That will make sure all the things you install are available to your code.

[^1]: You can actually put your virtual environment anywhere and name it anything, 
but I like to keep my virtual environment with my project.

#### Install NumPy
The library we need to get the drone flying is called NumPy. 
You can install by running this command (with your virtual environment activated, if you have one).
```shell
pip install numpy
```

#### Set Up Webots With Python
Now that you've installed that, Webots needs to have access to it.
If you didn't use a virtual environment, it may already work, 
but you can be certain by telling Webots where to look for your Python executable.

Go back to Webots. Open the Preferences window (⌘+, on macOS, Tools > Preferences on other platforms).

In the General tab, you'll find a field labeled "Python command." 
In it, enter `/path/to/your/project/folder/.venv/bin/python`, substituting the absolute path to your project.
If you put your virtual environment somewhere else, modify this path to reflec that.
If you didn't use a virtual environment at all, [this page](https://cyberbotics.com/doc/guide/using-python)
should give you some guidance on what to put here.

With that, you should be able to reload the project (the button with two arrows in a circle on the top toolbar)
and see your drone lift off. You should also be able to control it with your keyboard.

### Set Up An IDE
You can work directly in Webots on this project. 
In the side panel with a list of objects, click on the arrow next to 'Crazyflie "Crazyflie"',
select `controller`, and press Edit in the menu that appears below.

If you want to set up a different Python IDE for editing your project, [this page](https://cyberbotics.com/doc/guide/using-your-ide)
has info on setting up various IDEs. I also included instructions for PyCharm, which I personally used.
<details><summary><b>PyCharm</b></summary>
In the main settings window, under "Project: [Your Project Name]", select "Python Interpreter".
Hit "Add Interpreter > Add Local Interpeter...". Then click "Select existing" 
and set the "Python path" to `/path/to/your/virtual_environment/bin/python`.

After that go watch (and give a like to) [this video](https://www.youtube.com/watch?v=t6ZSB5cGZdQ&t=225)
that someone made on the full setup process. I found it useful through to about the 7-minute mark.
It is done for macOS, but it's likely a similar process on other platforms.

If you prefer to read, it is almost identical to the [aforementioned setup page](https://cyberbotics.com/doc/guide/using-your-ide#pycharm).
</details>

<details><summary><b>Emacs</b></summary>
Sorry Chris, I'm not figuring out how to make this one work just for you.
</details>

Give yourself a pat on the back. You've just finished all the setup you'll need.

