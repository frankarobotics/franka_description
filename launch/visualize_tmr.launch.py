import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    tmr_xacro_file = os.path.join(
        get_package_share_directory("franka_description"),
        "robots",
        "tmr",
        "tmr.urdf.xacro",
    )
    robot_description = Command([FindExecutable(name="xacro"), " ", tmr_xacro_file])

    rviz_filename_arg = DeclareLaunchArgument(
        'rviz_filename',
        default_value='tmr.rviz',
        description='Name of the rviz file that will be loaded'
    )

    rviz_filename = LaunchConfiguration('rviz_filename')

    rviz_file = PathJoinSubstitution([
        FindPackageShare("franka_description"),
        "rviz",
        rviz_filename,
    ])

    return LaunchDescription(
        [
            rviz_filename_arg,
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["--display-config", rviz_file],
            ),
        ]
    )
