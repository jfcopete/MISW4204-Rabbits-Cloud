#!/bin/bash
CONTAINER_NAME="dron_pg_container"
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB="dron_db"

docker exec -it $CONTAINER_NAME psql -U $POSTGRES_USER -p $POSTGRES_PASSWORD -d $POSTGRES_DB -f ./init.sql