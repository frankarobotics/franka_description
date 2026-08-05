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

END_EFFECTOR_IDS = [
    'franka_hand',
    'cobot_pump',
]


def get_urdf_xacro(robot_type: str):
    return path.join(
        get_package_share_directory('franka_description'),
        'robots',
        robot_type,
        robot_type + '.urdf.xacro',
    )


def get_end_effector_xacro(ee_id: str):
    return path.join(
        get_package_share_directory('franka_description'),
        'end_effectors',
        ee_id,
        ee_id + '.urdf.xacro',
    )


def get_srdf_xacro(robot_type: str):
    return path.join(
        get_package_share_directory('franka_description'),
        'robots',
        robot_type,
        robot_type + '.srdf.xacro',
    )


def get_link_names(root: ET.Element):
    return {link.get('name') for link in root.iter('link') if link.get('name')}


def get_referenced_links(srdf: ET.Element):
    """Return every link name an srdf refers to, whatever tag it appears in."""
    attributes = ('link1', 'link2', 'base_link', 'tip_link', 'parent_link', 'link')
    return {
        element.get(attribute)
        for element in srdf.iter()
        for attribute in attributes
        if element.get(attribute)
    }


def get_tcp_origin(root: ET.Element):
    """Return the xyz origin of the only tcp joint in a generated description."""
    joints = [
        joint
        for joint in root.iter('joint')
        if joint.get('name', '').endswith('_tcp_joint')
    ]
    assert len(joints) == 1, f'expected exactly one tcp joint, found {len(joints)}'
    return joints[0].find('origin').get('xyz')


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


@pytest.mark.parametrize('ee_id', END_EFFECTOR_IDS)
@pytest.mark.parametrize('robot_type', ARM_ROBOT_TYPES)
def test_tcp_offset_matches_end_effector(robot_type: str, ee_id: str):
    """A robot must place the tcp where the end effector alone would place it."""
    standalone = ET.fromstring(
        xacro.process_file(
            get_end_effector_xacro(ee_id), mappings={'ee_id': ee_id}
        ).toxml()
    )
    mounted = ET.fromstring(
        xacro.process_file(
            get_urdf_xacro(robot_type), mappings={'ee_id': ee_id}
        ).toxml()
    )
    assert get_tcp_origin(mounted) == get_tcp_origin(standalone)


@pytest.mark.parametrize('ee_id', END_EFFECTOR_IDS)
def test_tcp_offset_survives_direct_macro_use(ee_id: str, tmp_path):
    """Callers of the franka_robot macro must not silently lose the tcp offset."""
    caller = tmp_path / 'direct.urdf.xacro'
    caller.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="direct">\n'
        '  <xacro:include filename="$(find franka_description)'
        '/robots/common/franka_robot.xacro"/>\n'
        f'  <xacro:franka_robot robot_type="fr3" ee_id="{ee_id}" connected_to="base"/>\n'
        '</robot>\n'
    )
    standalone = ET.fromstring(
        xacro.process_file(
            get_end_effector_xacro(ee_id), mappings={'ee_id': ee_id}
        ).toxml()
    )
    direct = ET.fromstring(xacro.process_file(str(caller)).toxml())
    assert get_tcp_origin(direct) == get_tcp_origin(standalone)


@pytest.mark.parametrize('robot_type', ARM_ROBOT_TYPES)
def test_tcp_offset_can_be_overridden(robot_type: str):
    """An explicitly requested tcp offset must win over the end effector default."""
    urdf = xacro.process_file(
        get_urdf_xacro(robot_type), mappings={'tcp_xyz': '0 0 0.2'}
    ).toxml()
    assert get_tcp_origin(ET.fromstring(urdf)) == '0 0 0.2'


@pytest.mark.parametrize('no_prefix', ['false', 'true'])
@pytest.mark.parametrize('ee_id', END_EFFECTOR_IDS)
@pytest.mark.parametrize('robot_type', ARM_ROBOT_TYPES)
def test_every_joint_connects_existing_links(robot_type: str, ee_id: str, no_prefix: str):
    """A urdf is only loadable if every joint refers to links the urdf defines."""
    root = ET.fromstring(
        xacro.process_file(
            get_urdf_xacro(robot_type),
            mappings={'ee_id': ee_id, 'no_prefix': no_prefix},
        ).toxml()
    )
    links = get_link_names(root)
    for joint in root.iter('joint'):
        for end in ('parent', 'child'):
            referenced = joint.find(end).get('link')
            assert referenced in links, (
                f'joint {joint.get("name")} has {end} link {referenced}, '
                'which the urdf does not define'
            )


@pytest.mark.parametrize('no_prefix', ['false', 'true'])
@pytest.mark.parametrize('ee_id', END_EFFECTOR_IDS)
@pytest.mark.parametrize('robot_type', ARM_ROBOT_TYPES)
def test_srdf_only_refers_to_links_the_urdf_defines(
    robot_type: str, ee_id: str, no_prefix: str
):
    """An srdf that names a link absent from the urdf is rejected by MoveIt."""
    mappings = {'ee_id': ee_id, 'no_prefix': no_prefix}
    urdf = ET.fromstring(
        xacro.process_file(get_urdf_xacro(robot_type), mappings=mappings).toxml()
    )
    srdf = ET.fromstring(
        xacro.process_file(get_srdf_xacro(robot_type), mappings=mappings).toxml()
    )
    assert get_referenced_links(srdf) <= get_link_names(urdf)


if __name__ == '__main__':
    pytest.main([__file__])
