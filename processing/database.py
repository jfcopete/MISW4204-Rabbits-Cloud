
import os
from sqlmodel import SQLModel, create_engine
from libs.settings import traer_configuraciones

## connect to sqlLite
# directorio = os.path.abspath(os.getcwd())
# db_directorio = os.path.join(directorio, 'IDRL.db')
# engine = create_engine('sqlite:///' + db_directorio, echo=False)

## connect to postgres
configuraciones = traer_configuraciones()
pg_url = "postgresql://{}:{}@{}:{}/{}".format(
    configuraciones.DB_USER, configuraciones.DB_PASSWORD, configuraciones.DB_HOST, configuraciones.DB_PORT, configuraciones.DB_NAME
)
engine = create_engine(
    pg_url, echo=False
)

# valid for both sqlite and postgres
SQLModel.metadata.create_all(engine)

