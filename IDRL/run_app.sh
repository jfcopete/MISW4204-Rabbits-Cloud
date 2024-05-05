#!/bin/bash

IMAGE_NAME="rabbit-cloud" &&
docker build -t $IMAGE_NAME . &&
docker run --restart on-failure -p 8000:8000 $IMAGE_NAME -d