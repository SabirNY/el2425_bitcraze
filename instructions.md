#Instructions
## Flying
In order to hover you need to update the crazyflie firmware config. This is done by creating a config.mk file and place it inside `crazyflie-firmware/tools/make`. The file is now in this repo and consists only of two lines. The reason is to enable the kalman filter onboard the crazyflie. See [bitcraze wiki](https://wiki.bitcraze.io/doc:lps:index) for more information.

To understand the different steps it's important to distinguish between the different reference points.
First of all the crazyflie has an internal PID controller that receives a reference point along with the position estimate from the **lps-ros package**. This reference point is published on the **goal** topic. 

Secondly, we have implemented a higher level abstraction from this. The user instead specifies a **target point** representing the wanted position of the crazyflie. The reason for this is to be able to handle large step changes in the reference, keep constant velocity etc. When the user calls the `/crazyflie/set_target_position`, intermediate **goal points** are calculated and published on the **goal topic**. These are linearly interpolated between the previous target point and the new target point.

### Step 1

Call custom launch file connect.launch that takes a channel and address ending (the last two hexadecimal numbers) as input (defaults to `ch:=125 address:='E7'`) as well as initial target position (defaults to `x0:=0.0 y0:=1.5 z0:=1.5`). E.g.
```
roslaunch el2425_bitcraze connect.launch
```
to hover with crazyflie0  at `-1.0 1.0 1.5` or
```
roslaunch el2425_bitcraze connect.launch address:='BC' x0:=1.0 y0:=1.0 z0:=1.5
```
to hover with crazyflie1 at `1.0 1.0 1.5`.

### Step 2

Wait for a while for the filter to converge (check RViz).

### Step 3

Run `fly.py` to start hovering at initial target position.

```
rosrun el2425_bitcraze fly.py
```

### Step 4

To change the target position open a new terminal tab and call the `/crazyflie/set_target_position` service with x, y and z as arguments. **Important:** If you call the service with at least one negative input argument, you have to add ` -- ` before setting the argument
```
rosservice call /crazyflie/set_target_position x y z
```

Example:
```
rosservice call /crazyflie/set_target_position -- -1.0 1.0 1.0
```
The position can be changed by simply calling the `/set_target_position` service again.

### Step 5

Stop hovering by pressing `Enter` in the terminal where the fly.py script is running.

### Trajectory plotting
The reference trajectory and the corresponding crazyflie trajectory is plotted in RViz. The crazyflie trajectory is plotted once a target position has been set (by calling `/set_target_position`).

## Circular Path Following

Follow the step 1 to step 3 of Flying as described above.

### Step 4

Now to fly the UAV in a circle, call the service `set_polygon_trajectory`. The service takes three arguments, a list with the center of the circle, the radius and the angle in degrees w.r.t the x-axis. E.g. 
```
rosservice call /crazyflie/set_polygon_trajectory '[x0, y0, z0]' r0 theta0
```

## Multiple Flight
The multiple flight is very similar to flying with one crazyflie

### Step 1
Launch `connect_multiple.launch` wich takes the following arguments with specified default values
```
ch0:=125
address0:='E7'
x0:=0.0
y0:=1.5
z0:=1.5
ch1:=125
address1:='BC'
x1:=1.0
y1:=1.5
z1:=1.5
```
E.g.
```
roslaunch el2425_bitcraze connect_multiple.launch
```
to hover with crazyflie0 at `0.0 1.5 1.5` and crazyflie1 at `1.0 1.5 1.5`. 
### Step 2
Wait for filter convergence, check RViz

### Step 3
Run `fly_multiple.py`
```
rosrun el2425_bitcraze fly_multiple.py
```
### Step 4
Call `set_target_position` in corresponding namespace to publish a new target position for the crazyflies. To send crazyflie0 to `1.0 2.0 1.8` and crazyflie1 to `2.0 2.0 1.8` one would write (in a new terminal tab)
```
rosservice call /crazyflie0/set_target_position 1.0 2.0 1.8
rosservice call /crazyflie1/set_target_position 2.0 2.0 1.8
```
### Step 5
Switch to tab where `fly_multiple` is running and press `Enter` to land.

## Circular Path Following for Two Drones
You can follow the steps in folling a circular path for a single drone but calling the service with the appropriate
namespace. E.g.
```
rosservice call /crazyflie0/set_polygon_trajectory '[x0, y0, z0]' r0 theta0
rosservice call /crazyflie1/set_polygon_trajectory '[x1, y1, z1]' r0 theta1
```

We have also, for convenience, prepared a script that does a predefined path following for two drones. Try this out by running
```
rosrun el2425_bitcraze multi_circle_flight_test.py
```

Within this script there are the following lines that can be changed to specify new circluar paths for the drones.
```
setTrajectory0([0.0, 1.5, 1.5], 0.5, 90.0)
setTrajectory1([1.5, 1.5, 1.5], 0.5, 0.0)
```
## Data logging
The list of published data can be recorded in the data log file for analysis by following commands. First make a temprorary dircetory and then run rosbag record with the option -a which will record all the published topics in a bag file.
```
mkdir ~/bagfiles
cd ~/bagfiles
rosbag record -a
```
Exit the window with a Ctrl-C. You would see a file named with year, date and time in directory ~/bagfiles which contains all topics published bu any node.

After recording data run Matlab scrip "readrosbag.m" in Matlab with the required file name. You will observe plots for Crazflie x, y and z-positions with their respective means.
