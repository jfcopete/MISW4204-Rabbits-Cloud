import os
from sqlmodel import SQLModel, create_engine
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

# Función para obtener la URL de la base de datos
def get_connection():
    connector = Connector(ip_type=IPTypes.PUBLIC)  # o IPTypes.PRIVATE si estás usando IP privada
    instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name
    )
    return connection

# Configurar el motor de SQLAlchemy
engine = create_engine(
    "postgresql+pg8000://",
    creator=get_connection,
    echo=False
)

# Crear tablas
SQLModel.metadata.create_all(engine)



