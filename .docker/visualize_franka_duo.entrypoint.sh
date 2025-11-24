#!/bin/bash

args=$*
shift $#

cd /workspaces
colcon build --packages-select franka_description olv_module_descriptions > /dev/null
source install/setup.bash

ros2 launch franka_description visualize_franka_duo.launch.py ${args}