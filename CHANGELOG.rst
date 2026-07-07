^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package franka_description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.8.1 (2026-07-07)
------------------

* fix: define modified_prefix in tmrv0_2 description so mobile_teleop (robot_type tmrv0_2) renders

2.8.0 (2026-06-23)
------------------

* refactor: move ros2_control xacro content out of franka_description into franka_hardware (description is now distro-agnostic, free of ros2_control coupling)
* fix: corrected FR3 Duo mount angles in kinematics.yaml to match CAD values [51.18507533 deg, -10.00159382 deg, 26.54771649 deg]

2.7.1 (2026-05-04)
------------------

* fix: trigger workflow on X.Y.Z tags instead of v* prefix

2.7.0 (2026-05-04)
------------------

* feat: add GitHub Actions workflow to generate and release URDFs for fr3_duo, mobile_fr3_duo_v0_2, and fr3v2_1
* docu: Added the docu to FCI docs
* chore: Split the franka head, spine and mount out of fr3_duo/mobile_fr3_duo and adapted srdf
* fix: mobile_fr3_duo.urdf.xacro forwards is_async and thead_priority to ros2_control parts
* chore: refactored franka_arm.xacro configs
* fix: arm_prefixes index fixed for mfr3duo
* fix: corrected fr3_duo base mount for gazebo
* fix: tmr inertials updated
* feat: ros2 control file added for fr3 duo
* fix: mobile_fr3_duo.urdf.xacro forwards is_async and thead_priority to ros2_control parts
* feat: added mobile_fr3_duo_v0_2.srdf.xacro for moveit support and collision checking

2.6.0 (2026-03-02)
------------------
* feat: adaptations for gazebo
* fix: corrected accelerometer frames for fr3v1, fr3v2, fr3v2.1
* fix: properly handle arm_prefixes in srdf


2.5.0 (2026-02-17)
------------------

* chore: tmrv0_2 replace lidar with mounting point and add imu mounting point
* fix: mounting point typo in tmrv0_2.xacro
* feat: add the motor inertia and gear ratio to the urdfs of arms
* fix: adaptations for async control

2.4.0 (2026-01-26)
------------------

* feat: fr3_duo srdf added to franka description
* feat: fr3_duo urdf now supports different arm prefixes
* fix: removed olv_description_module dependency

2.3.2 (2026-01-22)
------------------

* chore: renamed meshes/robot_arms > meshes/robots to support tmr v0.2

2.3.1 (2026-01-16)
------------------
* feat: mobile_fr3_duo_v0_2 added to franka description

2.3.0 (2025-12-19)
------------------
* feat: tmrv0_2 added to franka description
* feat: arm_id replaced by robot_type
* feat: pass is_async argument to franka_arm.ros2_control.xacro
* feat: pass thread_priority argument to franka_arm.ros2_control.xacro
* feat: bump ros2_control version to 1.0.0

2.2.0
----------
* feat: updated kinematics, meshes, inertials, materials for fr3_duo mount and cover

2.1.0 (2025-10-24)
----------
* fix: add fp3 robot joint limits
* fix: group definition in SRDF file checking for right TCP
* feat: add fr3v2_1 robot variant

2.0.0 (2025-08-26)
------------------
* feat: migrate to ROS 2 Jazzy

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
