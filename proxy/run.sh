#!/bin/bash
# Convenience script for running docker container of this service.
FWD_TO_PORT="8081"
DOCKER_VOLUMES="${PWD}:/usr/src/app/etc/nginx"
DOCKER_IMG_TAG="${PWD##*/}:dev"

docker build -t $DOCKER_IMG_TAG . && \
docker run -p $FWD_TO_PORT:80 -v $DOCKER_VOLUMES $DOCKER_IMG_TAG
