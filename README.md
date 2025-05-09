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

## Create The AprilTag
AprilTags are an amazing little creation by the APRIL Robotics Laboratory that are like special QR codes for robots.
They're super easy and fast to track with a camera, even in 3D. If you're interested, you can learn more [here](https://april.eecs.umich.edu/software/apriltag).
I also find [this](https://docs.wpilib.org/en/stable/docs/software/vision-processing/apriltag/apriltag-intro.html) 
page in the FIRST Robotics WPILib Docs to be quite informative.
This will be what our drone tracks when flying.

![AprilTags on several small robots.](https://april.eecs.umich.edu/media/apriltag/apriltagrobots_overlay.jpg)

For the drone to track an AprilTag, it needs an AprilTag to track.

### Get An AprilTag
Go to [this](https://github.com/AprilRobotics/apriltag-imgs/tree/master/tag16h5) folder and choose an AprilTag.
The ID of each AprilTag is given in the last part of the file name (`tag16_05_[tag_id].png`).
You can choose any of these; just remember which tag you got.

When you click on the file, it will show a tiny preview. This is the actual size of the image, 
since they are scaled down to be just one pixel per square, resulting in an 8 pixel by 8 pixel image.
Download the one you chose using the download button.

Move this image to your `worlds` folder. 
I renamed mine to be something more typeable ([`apriltag1.png`](worlds/apriltag1.png)), but you don't have to.

### Insert The AprilTag
Now, we need to get it into our world.
Open up Webots. Make sure you pause and reset your simulation using the controls at the top of the window.
This takes several steps, so be patient, and go slowly.
> [!WARNING]
> Make sure that your drone is not currently flying and the time marker says 0:00:00:000.
> Otherwise, you won't be able to save your changes without overwriting the initial drone position. 

<details><summary>If you aren't patient, you can copy the final output here.</summary>

Copy this into the bottom of your `world.wbt` file

```
Robot {
  translation 0.5 0 1
  children [
    Solid {
      rotation 0 1 0 -1.5708
      children [
        Shape {
          appearance Appearance {
            texture ImageTexture {
              url [
                "[apriltag name].png"
              ]
              filtering 0
            }
          }
          geometry Plane {
            size 0.133333 0.133333
          }
        }
      ]
    }
  ]
  name "AprilTag"
}
```
Replace `[apriltag name]` with the name of your AprilTag image.

You can then reload your simulator (arrows in a circle icon) to see these changes.

---
</details>

1. Click on the plus button on the side menu showing all the world objects.
   Select "Base nodes > Robot" and hit Add.
2. Find that Robot in the sidebar. Expand its properties and scroll down to its "name" property.
   Change that to "AprilTag."
3. Find the "children" property on the Robot. Double-click on it to add a child.
   Find a "Solid" under "Base nodes" and add that.
4. Double-click the "children" property to add a "Shape" node (also under "Base nodes"; everything we're adding is) as a child of the Solid.
5. Add a "Plane" to the Shape node's "geometry" property.
   You should now see something gray flickering in the floor of the world.
6. Add an "Appearance" node to the Shape's "appearance" property.
7. Add an "ImageTexture" node to the Appearance's "texture" property.
8. Double-click on the ImageTexture's "url" property. 
   In the field that appears, type the name of the AprilTag you saved, including the .png extension.
   You should now see a blurry black and white image flickering in the floor.
9. Find the "rotation" property on the Shape node.
   Set the "y" property to 1 and the "x" and "z" properties to 0.
   Then set the "angle" property to -1.5708. 
   You should now see a blurry image of your AprilTag standing upright.
   If you right-click on the Solid and select "Move Viewpoint to Object", you can get a better view.
10. To solve the blurring problem, go back to the Image node and set its "filtering" property to 0.
    This will turn off smoothing of the PNG image, and you should now see your AprilTag in crisp detail.
11. Set the Plane's "size" property to x=0.133333 and y=0.133333. 
    This will make the inner part of the AprilTag 10 cm by 10 cm.
12. Go up to the Robot at the root named "AprilTag" and set it's "translation" property to x=0.5, y=0.0, z=1.0.
    This will position it about half a meter in front of the drone once it launches.

> [!WARNING]
> Make sure to save your changes using the save menu before doing anything else in the simulator.

Then, you can hit play and launch your drone.
It should come to rest with the AprilTag roughly centered in its camera window.

![The AprilTag centered in the drone's camera view](Pictures/apriltag_in_drone_view.jpg)

### Code The AprilTag
To make testing more interesting, this AprilTag will be able to move using keyboard controls 
so you can test the drone tracking it.

First, create a new folder called `apriltag_controller` in your `controllers` folder. 
This will store the code to implement these controls.

Next, create a new file in that folder called `apriltag_controller.py`.
As far as I can tell, controllers need to have the same name as their enclosing folder.

You can then copy the code in [this file](controllers/apriltag_controller/apriltag_controller.py).
It's heavily commented if you want to understand how it works, but generally not relevant to making this all work.

Finally, we need to wire up this controller with the AprilTag. Go back to Webots.
*Make sure* you've reset your simulation so you can make changes.
Then change two things in your "AprilTag" Robot.
1. Set the "controller" property to "apriltag_controller." The option should show up if you hit the Select button.
2. Set "supervisor" to TRUE. This allows the controller code to directly manipulate the simulations,
   which it needs to do to work.

If you save your changes and run the simulation, 
you should now be able to control the position of the AprilTag with similar controls to those of the Crazyflie.
Your Crazyflie may simultaneously be reacting to the keyboard inputs, because it's still set to use those controls.
Let's make it fly itself instead!

