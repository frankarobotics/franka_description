FROM osrf/ros:jazzy-desktop

ARG DEBIAN_FRONTEND=noninteractive

ARG USER_UID=1001
ARG USER_GID=1001
ARG USERNAME=user

WORKDIR /workspaces

# Delete existing user if it exists
RUN if getent passwd ${USER_UID}; then \
    userdel -r $(getent passwd ${USER_UID} | cut -d: -f1); \
    fi

# Delete existing group if it exists
RUN if getent group ${USER_GID}; then \
    groupdel $(getent group ${USER_GID} | cut -d: -f1); \
    fi

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir -p -m 0700 /run/user/"${USER_UID}" \
  && mkdir -p -m 0700 /run/user/"${USER_UID}"/gdm \
  && chown $USERNAME:$USERNAME /run/user/"${USER_UID}" \
  && chown $USERNAME:$USERNAME /workspaces \
  && chown $USERNAME:$USERNAME /run/user/"${USER_UID}"/gdm

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

USER $USERNAME

RUN echo "source /ros_entrypoint.sh" >>~/.bashrc
ARG MAX_ROS_DOMAIN_ID=232
RUN echo "export ROS_DOMAIN_ID=100" >>~/.bashrc
RUN echo "set +e" >>~/.bashrc
