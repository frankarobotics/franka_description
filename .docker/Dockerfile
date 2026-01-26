FROM osrf/ros:humble-desktop

ARG DEBIAN_FRONTEND=noninteractive

ARG USER_UID=1001
ARG USER_GID=1001
ARG USERNAME=user

WORKDIR /workspaces

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p -m 0700 /run/user/"${USER_UID}" \
    && mkdir -p -m 0700 /run/user/"${USER_UID}"/gdm \
    && chown user:user /run/user/"${USER_UID}" \
    && chown user:user /workspaces \
    && chown user:user /run/user/"${USER_UID}"/gdm 

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-humble-xacro \
    ros-humble-realsense2-description \
    ros-humble-joint-state-publisher-gui \
    ros-humble-realsense2-camera \
    ros-humble-sick-safetyscanners2 \
    ros-humble-robot-localization \
    && rm -rf /var/lib/apt/lists/*

ENV XDG_RUNTIME_DIR=/run/user/"${USER_UID}"

USER $USERNAME

RUN echo "source /ros_entrypoint.sh" >>~/.bashrc
ARG MAX_ROS_DOMAIN_ID=232
RUN echo "export ROS_DOMAIN_ID=100" >>~/.bashrc
RUN echo "set +e" >>~/.bashrc
