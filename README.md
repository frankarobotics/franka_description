# Franka Description

## Overview

The Franka Description repository offers all Franka Robotics models. It includes detailed 3D models and essential robot parameters, crucial for simulating these robots in various environments. Additionally, the repository provides a feature to create URDFs (Unified Robot Description Format) for the selected Franka robot model.

## Features

- **Comprehensive 3D Models**: Detailed 3D models of all Franka Robotics models for accurate simulation and visualization.
- **Robot Parameters**: All necessary robot parameters for realistic and reliable simulations.
- **URDF Creation**: Ability to create URDF files for any selected Franka robot model, essential for robot simulations in ROS and other robotic middleware.

## Prerequisites

- Docker

### URDF Creation

To start the generation, execute the start.sh script. The arguments passed to the sh script will be used from the create_urdf.py.

```
# Start the generation of the urdf model
./scripts/create_urdf.sh <robot_type> 
```

The urdf generation is performed by the create_urdf.py script which offers several parameters to customize the output urdf model:

```
usage: create_urdf.py [-h] [--robot-ee] [--no-ee] [--with-sc] [--abs-path] [--host-dir HOST_DIR] [--only-ee] [--no-prefix] robot_model

Generate franka robots urdf models. Script to be executed from franka_description root folder!

positional arguments:
  robot_model          id of the robot model (accepted values are: fr3v2_1, fr3v2, fr3, fp3, fer, fr3_duo, tmrv0_2, mobile_fr3_duo_v0_2, none)

optional arguments:
  -h, --help           show this help message and exit
  --robot-ee           id of the robot end effector (accepted values are: franka_hand, cobot_pump)
  --no-ee              Disable loading of end-effector (robot-ee would be ingnored if set) [WARNING: this argument will be removed in future releases, introducing "none" as ee id].
  --with-sc            Include self-collision volumes in the urdf model.
  --abs-path           Use absolute paths.
  --host-dir HOST_DIR  Provide a host directory for the absolute path.
  --only-ee            Get URDF with solely end-effector data
  --no-prefix          Override the robot prefix of links, joints and visuals in the urdf file.
```

### Visualize via ROS2

`franka_description` is offered as a ROS2 package.
The urdf file can be visualized via RViz with the following command:

```
# visualize_franka.sh launches the visualize_franka.launch.py in a ros2 instance running in the docker container
# The arguments given to the .sh script are forwarded as launch arguments
# Accepted launch arguments are:
#     robot_type - accepted values are: fr3v2_1, fr3v2, fr3, fp3, fer, fr3_duo, tmrv0_2, mobile_fr3_duo_v0_2
#     load_gripper - accepted values are: true (default ee_id is franka_hand), false (ee_id will be ignored) [WARNING: this argument will be removed in future releases, introducing "none" as ee id]
#     ee_id - accepted values are: franka_hand, cobot_pump

./scripts/visualize_franka.sh robot_type:=<robot_type> 

```
If you want to visualize the fr3 duo designed for multiple controller managers, the following command must be used:

```
./scripts/visualize_franka_duo.sh robot_type:=<robot_type> 
```

## Troubleshooting

### Figuring out your arm type

Identifying which arm type you have purchased is not always obvious, espcially for fr3, fr3v2 and fr3v2_1, as the differences are subtle. The easiest way is to check the arm type in Desk->Settings->Dashboard:

| franka_description | Desk      |
|--------------------|-----------|
| fp3                | Arm3P     |
| fr3                | Arm3R     |
| fr3v2              | Arm3Rv2   |
| fr3v2_1            | Arm3Rv2.1 |

If you have an fer or a system image older than 5.9.1 installed, the arm type my not be correctly displayed in Desk.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
