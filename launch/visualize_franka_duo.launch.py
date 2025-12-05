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

import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration


def robot_state_publisher_spawner(context: LaunchContext, robot_type, arm_prefix, load_gripper, ee_id):
    robot_type_str = robot_type
    arm_prefix_str = arm_prefix
    load_gripper_str = context.perform_substitution(load_gripper)
    ee_id_str = context.perform_substitution(ee_id)
    franka_xacro_filepath = os.path.join(
        get_package_share_directory('franka_description'),
        'robots',
        'fr3_duo',
        'fr3_duo_' + robot_type_str + '.urdf.xacro',
    )

    if robot_type_str == 'fixed_structure':
        robot_description = xacro.process_file(franka_xacro_filepath).toprettyxml(indent='  ')
    else:
        robot_description = xacro.process_file(
            franka_xacro_filepath,
            mappings={
                "hand": load_gripper_str,
                "ee_id": ee_id_str,
                "arm_prefix": arm_prefix_str
            }
        ).toprettyxml(indent="  ")

    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher_' + robot_type_str + '_' + arm_prefix_str,
            namespace=robot_type_str + '_' + arm_prefix_str,
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher_gui',
                namespace=robot_type_str + '_' + arm_prefix_str,
            ),
    ]


def generate_launch_description():
    load_gripper_parameter_name = "load_gripper"
    load_gripper = LaunchConfiguration(load_gripper_parameter_name)

    ee_id_parameter_name = "ee_id"
    ee_id = LaunchConfiguration(ee_id_parameter_name)

    robot_type_parameter_name = 'robot_type'
    robot_type = LaunchConfiguration(robot_type_parameter_name)

    rviz_file = os.path.join(
        get_package_share_directory("franka_description"),
        "rviz",
        "visualize_franka_duo.rviz",
    )

    robot_state_publisher_spawner_opaque_function = []
    fr3_duo_components = ["fixed_structure", "arm_left", "arm_right"]
    for component in fr3_duo_components:
        if component == "fixed_structure":
            print("Spawning fixed structure")
            robot_state_publisher_spawner_opaque_function.append(OpaqueFunction(
                function=robot_state_publisher_spawner, args=[component, "", load_gripper, ee_id]
            ))
        else:
            print('Spawning arm')
            robot_type = component.split('_')[0]
            arm_prefix = component.split('_')[1]
            robot_state_publisher_spawner_opaque_function.append(OpaqueFunction(
                function=robot_state_publisher_spawner,
                args=[robot_type, arm_prefix, load_gripper, ee_id]
            ))

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                load_gripper_parameter_name,
                default_value="true",
                description="Use end-effector if true. Default value is franka hand. "
                "Robot is loaded without end-effector otherwise",
            ),
            DeclareLaunchArgument(
                ee_id_parameter_name,
                default_value="franka_hand",
                description="ID of the type of end-effector used. Supporter values: "
                "none, franka_hand, cobot_pump",
            ),
            DeclareLaunchArgument(
                robot_type_parameter_name,
                description='ID of the type of arm used. Supporter values: '
                'fr3_duo',
            ),
            *robot_state_publisher_spawner_opaque_function,
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["--display-config", rviz_file],
            ),
        ]
    )
