
import os
from sqlmodel import SQLModel, create_engine

directorio = os.path.abspath(os.getcwd())
db_directorio = os.path.join(directorio, 'IDRL.db')

engine = create_engine('sqlite:///' + db_path, echo=False)

SQLMODEL.metadata.create_all(engine)

