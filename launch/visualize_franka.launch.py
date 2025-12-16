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


def resolve_rviz_config(context: LaunchContext, rviz_file_config):
    """Resolve RViz config to full path. Supports both filename and full path."""
    rviz_file_str = context.perform_substitution(rviz_file_config)
    
    if os.path.isabs(rviz_file_str):
        return rviz_file_str
    
    return os.path.join(
        get_package_share_directory("franka_description"),
        "rviz",
        rviz_file_str
    )


def robot_state_publisher_spawner(context: LaunchContext, robot_type, load_gripper, ee_id):
    robot_type_str = context.perform_substitution(robot_type)
    load_gripper_str = context.perform_substitution(load_gripper)
    ee_id_str = context.perform_substitution(ee_id)
    franka_xacro_filepath = os.path.join(
        get_package_share_directory('franka_description'),
        'robots',
        robot_type_str,
        robot_type_str + '.urdf.xacro',
    )
    robot_description = xacro.process_file(
        franka_xacro_filepath, mappings={"hand": load_gripper_str, "ee_id": ee_id_str}
    ).toprettyxml(indent="  ")

    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description}],
        )
    ]


def rviz_spawner(context: LaunchContext, rviz_file_config):
    rviz_config_path = resolve_rviz_config(context, rviz_file_config)
    
    return [
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["--display-config", rviz_config_path],
        )
    ]


def generate_launch_description():
    load_gripper_parameter_name = "load_gripper"
    load_gripper = LaunchConfiguration(load_gripper_parameter_name)

    ee_id_parameter_name = "ee_id"
    ee_id = LaunchConfiguration(ee_id_parameter_name)

    robot_type_parameter_name = 'robot_type'
    robot_type = LaunchConfiguration(robot_type_parameter_name)

    rviz_file_parameter_name = 'rviz_file'
    rviz_file = LaunchConfiguration(rviz_file_parameter_name)

    robot_state_publisher_spawner_opaque_function = OpaqueFunction(
        function=robot_state_publisher_spawner, args=[robot_type, load_gripper, ee_id]
    )
    
    rviz_spawner_opaque_function = OpaqueFunction(
        function=rviz_spawner, args=[rviz_file]
    )

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
                'fer, fr3, fp3, fr3v2, fr3v2_1, tmrv0_2',
            ),
            DeclareLaunchArgument(
                rviz_file_parameter_name,
                default_value="visualize_franka.rviz",
                description="Name of the RViz configuration file "
                "(if located in franka_description/rviz folder) or as absolute path",
            ),
            robot_state_publisher_spawner_opaque_function,
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
            ),
            rviz_spawner_opaque_function,
        ]
    )
