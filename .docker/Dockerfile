FROM osrf/ros:jazzy-desktop

ARG DEBIAN_FRONTEND=noninteractive

ARG USER_UID=1001
ARG USER_GID=1001
ARG USERNAME=user

WORKDIR /workspaces

# The base image already ships a user and group at UID/GID 1000, so only
# create ours when the host UID/GID is still free.
RUN (getent group $USER_GID || groupadd --gid $USER_GID $USERNAME) \
    && (getent passwd $USER_UID || useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME) \
    && mkdir -p -m 0700 /run/user/"${USER_UID}" \
    && mkdir -p -m 0700 /run/user/"${USER_UID}"/gdm \
    && chown $USER_UID:$USER_GID /run/user/"${USER_UID}" \
    && chown $USER_UID:$USER_GID /workspaces \
    && chown $USER_UID:$USER_GID /run/user/"${USER_UID}"/gdm

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-jazzy-xacro \
    ros-jazzy-realsense2-description \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-realsense2-camera \
    ros-jazzy-sick-safetyscanners2 \
    ros-jazzy-robot-localization \
    && rm -rf /var/lib/apt/lists/*

ENV XDG_RUNTIME_DIR=/run/user/"${USER_UID}"

# Address the account by UID:GID, it may pre-exist under a different name.
USER $USER_UID:$USER_GID

RUN echo "source /ros_entrypoint.sh" >>~/.bashrc
ARG MAX_ROS_DOMAIN_ID=232
RUN echo "export ROS_DOMAIN_ID=100" >>~/.bashrc
RUN echo "set +e" >>~/.bashrc
