#  Copyright (c) 2026 Franka Robotics GmbH
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
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory

import pytest
import xacro

ARM_ROBOT_TYPES = [
    'fer',
    'fp3',
    'fr3',
    'fr3v2',
    'fr3v2_1',
]

ROBOT_TYPES = ARM_ROBOT_TYPES + ['tmrv0_2', 'fr3_duo', 'mobile_fr3_duo_v0_2']


def get_urdf_xacro(robot_type: str):
    return path.join(
        get_package_share_directory('franka_description'),
        'robots',
        robot_type,
        robot_type + '.urdf.xacro',
    )


@pytest.mark.parametrize('include_self_collision_geometry', ['true', 'false'])
@pytest.mark.parametrize('robot_type', ROBOT_TYPES)
def test_urdf_is_well_formed(robot_type: str, include_self_collision_geometry: str):
    urdf = xacro.process_file(
        get_urdf_xacro(robot_type),
        mappings={
            'with_sc': 'true',
            'include_self_collision_geometry': include_self_collision_geometry,
        },
    ).toxml()
    root = ET.fromstring(urdf)
    assert root.tag == 'robot', 'urdf must have topmost level robot tag'
    assert len(root) > 0, 'urdf cannot be empty'


@pytest.mark.parametrize('robot_type', ARM_ROBOT_TYPES)
def test_without_ee(robot_type: str):
    """Test of hand parameter equal to none."""
    urdf = xacro.process_file(
        get_urdf_xacro(robot_type),
        mappings={
            'ee_id': 'none',
        },
    ).toxml()
    root = ET.fromstring(urdf)
    assert root.find(f".//joint[@name='{robot_type}_finger_joint1']") is None
    assert root.find(f".//joint[@name='{robot_type}_finger_joint2']") is None


@pytest.mark.parametrize('robot_type', ARM_ROBOT_TYPES)
def test_with_ee(robot_type: str):
    """Test of hand parameter equal to a value."""
    urdf = xacro.process_file(
        get_urdf_xacro(robot_type), mappings={'ee_id': 'franka_hand'}
    ).toxml()
    root = ET.fromstring(urdf)
    assert root.find(f".//joint[@name='{robot_type}_finger_joint1']") is not None, (
        'urdf must contain the finger 1 joint tag'
    )
    assert root.find(f".//joint[@name='{robot_type}_finger_joint2']") is not None, (
        'urdf must contain the finger 2 joint tag'
    )


if __name__ == '__main__':
    pytest.main([__file__])
