#!/bin/bash

args=$*
shift $#

source /ros_entrypoint.sh

cd /workspaces
colcon build --packages-select franka_description olv_module_descriptions > /dev/null
source install/setup.bash

cd src/franka_description

python3 scripts/create_urdf.py $args