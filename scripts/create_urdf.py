#  Copyright (c) 2024 Franka Robotics GmbH
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

import argparse
import os

import xacro


def str_to_bool(s):
    return s.lower() in ["true", "1", "yes", "y"]


def convert_xacro_to_urdf(xacro_file, only_ee, with_sc, ee_id, hand, no_prefix, robot):
    """Convert xacro file into a URDF file."""
    mappings = {
        'with_sc': str(with_sc),
        'ee_id': str(ee_id),
        'hand': str(hand),
        'no_prefix': str(no_prefix),
        'robot_type': str(robot),
    }

    if only_ee and robot == "":
        mappings["connection"] = ""

    urdf = xacro.process_file(xacro_file, mappings=mappings)
    urdf_file = urdf.toprettyxml(indent="  ")
    return urdf_file


def convert_package_name_to_absolute_path(package_name, package_path, urdf_file):
    """Replace a ROS package names with the absolute paths."""
    urdf_file = urdf_file.replace("package://{}".format(package_name), package_path)
    return urdf_file


def urdf_generation(
    package_path,
    xacro_file,
    file_name,
    ONLY_EE,
    WITH_SC,
    EE,
    HAND,
    NO_PREFIX,
    robot,
    description_type="urdf",
):
    """Generate URDF file and save it."""
    xacro_file = os.path.join(package_path, xacro_file)
    urdf_file = convert_xacro_to_urdf(xacro_file, ONLY_EE, WITH_SC, EE, HAND, NO_PREFIX, robot)
    if ABSOLUTE_PATHS and (HOST_DIR is None or HOST_DIR == ""):
        urdf_file = convert_package_name_to_absolute_path(package_name, package_path, urdf_file)
    elif ABSOLUTE_PATHS:
        urdf_file = convert_package_name_to_absolute_path(package_name, HOST_DIR, urdf_file)
    save_urdf_to_file(package_path, urdf_file, file_name, description_type)


def save_urdf_to_file(package_path, urdf_file, robot, description_type="urdf"):
    """Save URDF into a file."""
    # Check if the folder exists, and if not, create it
    folder_path = f"{package_path}/urdfs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(f"{package_path}/urdfs/{robot}.{description_type}", "w") as f:
        f.write(urdf_file)


if __name__ == "__main__":
    package_name = "franka_description"

    if os.getcwd().split("/")[-1] != package_name:
        print("Call the script from franka_description root folder")
        exit()

    ROBOTS = ['fr3v2_1', 'fr3v2', 'fr3_duo', 'fr3', 'fp3', 'fer', 'tmrv0_2', 'mobile_fr3_duo_v0_2']
    ROBOTS_WITHOUT_SRDF = ['fr3_duo', 'tmrv0_2', 'mobile_fr3_duo_v0_2']

    END_EFFECTORS = ["none", "franka_hand", "cobot_pump"]

    parser = argparse.ArgumentParser(
        description="""
            Generate franka robots urdf models.
            Script to be executed from franka_description root folder!
            """
    )

    robots_str = ", ".join([f"{item}" for item in ROBOTS])
    parser.add_argument(
        "robot_model",
        type=str,
        nargs="?",
        default="",
        help="id of the robot model (accepted values are: {})".format(robots_str),
    )
    parser.add_argument(
        "--no-ee",
        help="Disable loading of end-effector.",
        action="store_const",
        const=True,
    )
    ee_str = ", ".join([f"{item}" for item in END_EFFECTORS])
    parser.add_argument(
        "--robot-ee",
        type=str,
        default="franka_hand",
        help="id of the robot end effector (accepted values are: {})".format(ee_str),
    )
    parser.add_argument(
        "--with-sc",
        help="Include self-collision volumes in the urdf model.",
        action="store_const",
        const=True,
    )
    parser.add_argument("--abs-path", help="Use absolute paths.", action="store_const", const=True)
    parser.add_argument("--host-dir", help="Provide a host directory for the absolute path.")
    parser.add_argument(
        "--only-ee",
        help="Get urdf with solely end-effector data.",
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--no-prefix",
        help="Override the robot prefix of links, joints and visuals in the urdf file.",
        action="store_const",
        const=True,
    )

    args = parser.parse_args()

    ROBOT_MODEL = args.robot_model.lower()
    HAND = not args.no_ee
    EE = args.robot_ee.lower() if args.robot_ee is not None else "franka_hand"
    WITH_SC = args.with_sc if args.with_sc is not None else False
    ABSOLUTE_PATHS = args.abs_path if args.abs_path is not None else False
    HOST_DIR = args.host_dir
    ONLY_EE = args.only_ee if args.only_ee is not None else False
    NO_PREFIX = args.no_prefix if args.no_prefix is not None else "false"

    assert (
        ROBOT_MODEL in ROBOTS or ROBOT_MODEL == "all" or ROBOT_MODEL == "none" or ROBOT_MODEL == ""
    )

    if ROBOT_MODEL != "all" and ROBOT_MODEL != "none":
        ROBOTS = [ROBOT_MODEL]

    package_path = os.getcwd()
    if ONLY_EE:
        print(f"\n*** Creating URDF for {EE} ***")
        xacro_file = f"end_effectors/{EE}/{EE}.urdf.xacro"
        file_name = f"{EE}"
        if ROBOT_MODEL == "all" or ROBOT_MODEL == "none" or ROBOT_MODEL == "":
            robot_prefix = ""
        else:
            robot_prefix = ROBOT_MODEL
        urdf_generation(
            package_path,
            xacro_file,
            file_name,
            ONLY_EE,
            WITH_SC,
            EE,
            HAND,
            NO_PREFIX,
            robot_prefix,
        )
    else:
        if ROBOT_MODEL == "none" or ROBOT_MODEL == "":
            print("\n*** Robot model must be specified ***")
        else:
            for robot in ROBOTS:
                description_types = ["urdf", "srdf"]
                for description_type in description_types:
                    if description_type == 'srdf' and robot in ROBOTS_WITHOUT_SRDF:
                        # write dummy srdf file
                        print(f'\n*** Creating dummy {description_type} for {robot} ***')
                        file_name = f'{robot}'
                        save_urdf_to_file(
                            package_path,
                            f'<robot name="{robot}"></robot>',
                            file_name,
                            description_type,
                        )
                        continue
                    xacro_file = f'robots/{robot}/{robot}.{description_type}.xacro'
                    if HAND and EE != 'none' and robot != 'tmrv0_2':
                        print(f'\n*** Creating {description_type} for {robot} and {EE} ***')
                        file_name = f'{robot}_{EE}'
                    else:
                        if not HAND or robot == 'tmrv0_2':
                            print(
                                "\n*** WARNING: --no-ee argument will be removed in future"
                                " releases, introducing none as ee id***"
                            )
                        print(f"\n*** Creating {description_type} for {robot} ***")
                        file_name = f"{robot}"
                    urdf_generation(
                        package_path,
                        xacro_file,
                        file_name,
                        ONLY_EE,
                        WITH_SC,
                        EE,
                        HAND,
                        NO_PREFIX,
                        robot,
                        description_type,
                    )
