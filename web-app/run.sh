#!/bin/bash
# Convenience script for running docker container of this service.
FWD_TO_PORT="8080"
DOCKER_VOLUMES="${PWD}/app/src:/usr/src/app/src:ro"
DOCKER_IMG_TAG="${PWD##*/}:dev"

docker build -t $DOCKER_IMG_TAG -f Dockerfile.dev . && \
docker run -p $FWD_TO_PORT:80 -v $DOCKER_VOLUMES $DOCKER_IMG_TAG\
              npm run start -- --host --poll 500 --port 80
