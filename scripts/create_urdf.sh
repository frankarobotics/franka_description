#!/usr/bin/env bash

docker build -t urdf_creation \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    ./.docker

echo 

docker run -u $(id -u) \
    -v "$(pwd):/workspaces/src/franka_description" \
    -w /workspaces/src/franka_description \
    urdf_creation \
    .docker/create_urdf.entrypoint.sh $*
