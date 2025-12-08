#  Copyright (c) 2023 Franka Robotics GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from os import path

import xacro
from ament_index_python.packages import get_package_share_directory

robot_type_ = 'fer'

xacro_file_name = path.join(
    get_package_share_directory('franka_description'),
    'robots',
    robot_type_,
    robot_type_ + '.urdf.xacro',
)


def test_load():
    """Test of hand parameter equal to none."""
    urdf = xacro.process_file(
        xacro_file_name,
        mappings={
            'robot_type': 'fer',
            'ee_id': 'none',
        },
    ).toxml()
    assert urdf.find("fer_finger_joint1") == -1


def test_load_with_gripper():
    """Test of hand parameter equal to a value."""
    urdf = xacro.process_file(
        xacro_file_name, mappings={'robot_type': 'fer', 'ee_id': 'franka_hand'}
    ).toxml()
    assert urdf.find("fer_finger_joint") != -1


def test_check_interfaces():
    """Test of the parameters for ros2_control hardware interface."""
    urdf = xacro.process_file(
        xacro_file_name, mappings={"ros2_control": "true"}
    ).toxml()
    assert urdf.find("state_interface") != -1
    assert urdf.find("command_interface") != -1
    assert urdf.find("position") != -1
    assert urdf.find("velocity") != -1
    assert urdf.find("effort") != -1


def test_load_with_fake_hardware():
    """Test of use_fake_hardware parameter for ros2_control hardware interface."""
    urdf = xacro.process_file(
        xacro_file_name, mappings={"ros2_control": "true", "use_fake_hardware": "true"}
    ).toxml()
    assert urdf.find("fake_components/GenericSystem") != -1


def test_load_with_robot_ip():
    """Test of robot_ip parameter for ros2_control hardware interface."""
    urdf = xacro.process_file(
        xacro_file_name,
        mappings={"ros2_control": "true", "robot_ip": "franka_ip_address"},
    ).toxml()
    assert urdf.find("franka_ip_address") != -1


if __name__ == "__main__":
    pass
