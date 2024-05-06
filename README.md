# MISW4204-Rabbits-Cloud

Repositorio de Equipo (Rabbit) para el curso MISW4203 Desarrollo de software en la nube

## Projecto en nube

Este proyecto está alojado en Máquinas Virtual (VM) en Google Cloud Platform (GCP) y se puede acceder a través del balanceador de carga con la dirección IP 34.160.67.217. Dentro del repositorio, encontrarás las colecciones de Postman listas para ser importadas y utilizadas.

## Iniciar el projecto en local

### Descripción de Componentes

**IDRL (servicio REST API)**: Este servicio gestiona las solicitudes (CRUD) relacionadas con el negocio, autenticación, consultas de estados y carga de videos. Está conectado a Google Cloud y utiliza Cloud SQL para el almacenamiento de datos.
**Kafka (cola de mensajes)**: Se utiliza como un conector asíncrono entre el servicio IDRL y Processing para la comunicación de mensajes.
**PostgreSQL**: Base de datos relacional utilizada para almacenar datos relacionados con el proyecto.
**Processing**: Este servicio está dedicado al procesamiento de videos, incluida la edición. Al igual que IDRL, está conectado a Google Cloud y utiliza Cloud SQL para el almacenamiento de datos.

### Requisitos

- Docker
- docker compose

### Comandos de inicio

El proyecto está organizado en cuatro carpetas, una para cada uno de los proyectos mencionados:

**IDRL:** Contiene el archivo run_app.sh, que se utiliza para ejecutar el servicio REST API.
**Kafka:** Contiene el archivo run_app.sh, que se utiliza para ejecutar el servicio de cola de mensajes Kafka.
**PostgreSQL:** Contiene el archivo run_app.sh, que se utiliza para ejecutar la base de datos PostgreSQL.
**Processing:** Contiene el archivo run_app.sh, que se utiliza para ejecutar el servicio de procesamiento de videos.

**Consideraciones Individuales:**

Es esencial seguir un orden específico al iniciar los servicios. La base de datos y el servicio de colas deben iniciarse antes que los servicios del API y el procesador de videos, ya que estos últimos dependen de que los primeros estén disponibles para su ejecución.

**Kafka:**

Dirígete a la carpeta _kafka_ y ejecuta el script `bash run_app.sh`.

**PostgreSQL:**

Dirígete a la carpeta _postgress_ y ejecuta el script `bash run_app.sh`.

(Opcional) Si deseas inicializar la base de datos, puedes conectarla mediante un PgAdmin u otro visor de tu preferencia, y ejecutar las sentencias que se encuentran en el archivo `init_db.sql`.

**IDRL:**

Entra en la carpeta IDRL y asegúrate de agregar los siguientes archivos:

- _.env_ en la raíz del proyecto IDRL
- _vinilos-bk-988ea0e24d53.json_ dentro de la carpeta _IDRL/libs/_

Luego, ejecuta el comando `bash run_app.sh`.

**Processing:**

Ingresa en la carpeta processing y asegúrate de agregar los siguientes archivos:

- _.env_ en la raíz del proyecto processing
- _vinilos-bk-988ea0e24d53.json_ dentro de la carpeta processing/libs/

Finalmente, ejecuta el comando `bash run_app.sh`.

**Nota:** Por motivos de seguridad, se han utilizado variables de entorno. Por favor, solicita estas variables a algún miembro del equipo y serán enviadas por correo electrónico.

## Documentación de los endpoints

Para acceder a la documentación después de haber iniciado el proyecto, dirígete a la siguiente ruta:

- Localmente: [http://localhost:8000/docs#/](http://localhost:8000/docs#/)
- En línea: [http://34.160.67.217/docs](http://34.160.67.217/docs)
