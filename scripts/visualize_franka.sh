#!/usr/bin/env bash

docker build -t urdf_creation \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    ./.docker

echo 

docker run -it -u $(id -u) \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=${DISPLAY} \
    -v $(pwd):/workspaces/src/franka_description \
    -w /workspaces/src/franka_description \
    urdf_creation \
    .docker/visualize_franka.entrypoint.sh $*