# MISW4204-Rabbits-Cloud

Repositorio de Equipo (Rabbit) para el curso MISW4203 Desarrollo de software en la nube

## Despliegue en PaaS. Migración de la aplicación WEB a plataforma como servicio en la nube pública.

El proyecto esta desplegado en su totalidad en la nube pública de Google Cloud Platform (GCP). 

Para la capa WEB se cuenta con un servicio de Cloud Rud disponible en la ruta: `https://app-sql-v1-cx5bp6smwq-uc.a.run.app`.
Este servicio cuenta todas las funcionalidades de la capa WEB incluyendo Login, carga de objetos (video original) a Cloud Storage, escritura y lectura de datos de tareas de procesamiento en servicio de base de datos de Cloud SQL, envío de mensaje a Cloud Pub/Sub para comunicación asincrona con la capa WORKER, eliminación de tareas que ya esten procesadas en la base de datos y eliminación de objetos (video original y editado) de Cloud Storage.

Para la capa WORKER se cuenta con un servicio de Cloud Run, este servicio recibe solicitudes http de una subscripción tipo PUSH configurada en Cloud Pub/Sub, con cada solicitud ejecuta una tarea de procesamiento de un video, al finalizar almacena el objeto (video editado) en el bucket de Cloud Storage y modifica los datos de la tarea de procesamiento correspondiente en el servicio de base de datos de Cloud SQL.

### Imagenes docker

Cada servicio Cloud Run cuenta con una imagen docker desplegada, estas imagenes estan almacenadas en `Artifact Registry` de `Cloud GCP`
El servicio correspondiente a la capa WEB tiene la imagen docker generada por el archivo: `IDRL/Dockerfile` del repositorio en la rama `app_sql`.
El servicio correspondiente a la capa WORKER tiene la imagen docker generada por el archivo: `processing/Dockerfile` del repositorio en la rama `app_sql`.

### Requisitos para usar la aplicación.

- Postman para realizar las peticiones.
- Base de datos de Cloud SQL aprovisionada en el proyecto. (La base de datos se ha eliminado por el presupuesto limitado). 

### Comandos de inicio

En caso de requerir el uso de la aplicación, por favor comunicarse con el equipo para aprovisionar la base de datos.

## Documentación de APIs

Para acceder a la documentación de la API de la capa WEB `https://app-sql-v1-cx5bp6smwq-uc.a.run.app/docs#/`
Para acceder a la documentación de la API de la capa WORKER `https://processing-sql-v1-cx5bp6smwq-uc.a.run.app/docs#/`

