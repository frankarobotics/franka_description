^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package franka_description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.5.3 (2026-02-26)
----------
* fix: removed `olv_descriptions_module` dependency completely
* chore: tmrv0_2 replace lidar with mounting point and add imu mounting point
* fix: mounting point typo in tmrv0_2.xacro

1.5.2 (2026-01-22)
----------
* chore: renamed meshes/robot_arms > meshes/robots to support tmr v0.2

1.5.1 (2026-01-16)
----------
* feat: mobile_fr3_duo_v0_2 added to franka description

1.5.0 (2025-12-19)
----------
* feat: tmrv0_2 added to franka description
* feat: arm_id replaced by robot_type
* feat: add RViz config path as launch parameter to visualize_franka.launch.py

1.4.0 (2025-11-10)
----------
* feat: updated kinematics, meshes, inertials, materials for fr3_duo mount and cover

1.3.0 (2025-10-31)
------------------
* fix: group definition in SRDF file checking for right TCP
* feat: add fr3v2_1 robot variant

1.2.0 (2025-10-24)
------------------
* fix: add fp3 robot joint limits

1.1.0
----------
* feat: added accelerometer frames to urdfs
* feat: update joint limits for fr3v2 and fr3
* feat: add position based velocity limits tags to urdfs for fr3v2 and fr3

1.0.2 (2025-08-01)
---------------
* fix: gazebo can be used with prefixes
* fix: ee_with_one_link takes the correct arguments to allow visualization

1.0.1 (2025-07-09)
---------------
* fix: cover and mount replaced by new designs

1.0.0 (2025-06-26)
---------------
* breaking change: cobot pump parameters are not longer selected by default in the robot xacro
* fix: urdf xacros include end-effector parameters

0.5.1 (2025-03-19)
---------------
* feature: fr3 duo added to franka description
* feature: Added additional command interfaces for FX3 to the URDF
* feature: identify fr3v2 inertials
* feature: add the version tag to ros2_control
* fix: change paramater location in xacro/macro from arg to property

0.5.0 (2025-03-07)
---------------
* feature: Added prefix to single robot control
* fix: hand inertials fixed
* feature: add srdfs for arms and hand
* feature: add fr3v2 robot

0.4.0 (2024-12-11)
------------------
* feature: no prefix option added
* fix: use phong instead of lambert shading
* fix: script create_urdf.sh needs the correct user id
* feature: adding the .xacro definition for multi arm setups

0.3.0 (2024-11-27)
------------------
* feature: franka_ign_ros2_control plugin for gazebo
* feature: gazebo simulation joint friction and gazebo effort interface param
* feature: support gazebo simulation in ros2
* fix: rpy values added
* fix: link0 inertials added
* fix: formatting python
* fix: gazebo ros2 plugin name
* change: changed minor principal moment of inertia to satisfy triangle inequality
* other: Update copyright date
* Contributors: Andreas Kuhner, Baris Yazici, Guillermo Gomez Pena, Marius Winkelmeier

0.2.0 (2024-05-21)
------------------

* feat: end-effector can be deactivated with an argument
* feat: add dedicated folder for end-effectors
* fix: license name in readme
* Contributors: Guillermo Gomez Pena

0.1.10 (2024-04-22)
-------------------

0.1.0 (2024-01-26)
------------------
* Publish franka_description
* Contributors: Baris Yazici, Enrico Sartori
