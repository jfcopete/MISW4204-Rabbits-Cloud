#!/bin/bash

# Eliminar archivos de kafka
rm -rf /bitnami

# Eliminar contenedores
docker compose down

# Correr los contenedores
docker compose up zookeeper -d
sleep 10
docker compose up kafka -d
sleep 10
docker compose up kafdrop -d
sleep 10
docker compose up postgres-db -d
sleep 10
docker compose up processing -d
sleep 10
docker compose up storage -d
sleep 10
docker compose up idrl -d --build --force-recreate