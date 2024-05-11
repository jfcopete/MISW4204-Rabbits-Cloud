#!/bin/bash

IMAGE_NAME="rabbit-cloud" &&
docker build -t $IMAGE_NAME . &&
docker run --restart on-failure --env-file .env -p 8000:8000 -d $IMAGE_NAME 

# #!/bin/bash

# IMAGE_NAME="rabbit-cloud"

# # Eliminar la imagen existente si existe
# docker image rm $IMAGE_NAME

# # Construir la imagen Docker
# docker build --no-cache -t $IMAGE_NAME .

# # Ejecutar el contenedor Docker
# docker run --env-file .env -p 8000:8000 $IMAGE_NAME
