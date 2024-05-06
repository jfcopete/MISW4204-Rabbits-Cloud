#!/bin/bash

CONTAINER_NAME="dron_pg_container"
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB="dron_db"
VOLUME_NAME="pgdata"

if [ $(docker volume ls -q -f name=$VOLUME_NAME) ]; then
    echo "Volume $VOLUME_NAME already exists."
else
    docker volume create $VOLUME_NAME
    echo "Volume $VOLUME_NAME created."
fi

docker pull postgres:13.3

# Run container
docker run --name $CONTAINER_NAME -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB -v $VOLUME_NAME:/var/lib/postgresql/data -p 5432:5432 -d postgres:13.3