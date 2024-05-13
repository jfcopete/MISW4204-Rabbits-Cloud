#!/bin/bash

IMAGE_NAME="rabbit-cloud-processor" &&
docker build -t $IMAGE_NAME . &&
docker run --restart on-failure --env-file .env -d $IMAGE_NAME