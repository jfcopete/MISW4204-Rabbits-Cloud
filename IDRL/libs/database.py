
import os
from sqlmodel import SQLModel, create_engine

directorio = os.path.abspath(os.getcwd())
db_directorio = os.path.join(directorio, 'IDRL.db')

engine = create_engine('sqlite:///' + db_directorio, echo=False)

SQLModel.metadata.create_all(engine)

