#!/bin/bash

# Eliminar archivos de kafka
rm -rf /bitnami

# Eliminar contenedores
docker compose down

# Correr los contenedores
docker compose up