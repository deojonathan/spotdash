#!/bin/bash
# Convenience script for running docker container of this service.
GUNICORN_APP="gunicorn"
GUNICORN_ARGS="--bind 0.0.0.0:80 -w 4 --reload app:app"
FWD_TO_PORT="8081"

DOCKER_VOLUMES="app:/usr/src/app"
DOCKER_IMG_TAG="auth-server:dev"

docker build -t $DOCKER_IMG_TAG . && \
docker run -p $FWD_TO_PORT:80 -v $DOCKER_VOLUMES $DOCKER_IMG_TAG \
              $GUNICORN_APP $GUNICORN_ARGS
