
import os
from sqlmodel import SQLModel, create_engine

directorio = os.path.abspath(os.getcwd())
db_directorio = os.path.join(directorio, 'IDRL.db')

pg_url = "postgresql://{}:{}@{}:{}/{}".format(
    # "postgres", "postgres", "postgres-db", 5432, "dron_db"
    "postgres", "Password!", "35.238.92.63", 5432, "dbrabbitscloud"
    # service-account-rabbit-cloud
)

# engine = create_engine('sqlite:///' + db_directorio, echo=False)
engine = create_engine(
    pg_url, echo=False
)



SQLModel.metadata.create_all(engine)

