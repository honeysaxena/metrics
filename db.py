import pathlib
#from cassandra.cluster import Cluster
#from cassandra.auth import PlainTextAuthProvider
#from cassandra.cqlengine import connection
from application import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = pathlib.Path(__file__).resolve().parent
print(BASE_DIR)

settings = config.get_settings()



#ASTRADB_CONNECT_BUNDLE = BASE_DIR / "connect_bundle" / "astradb_connect.zip"
#ASTRADB_CLIENT_ID = settings.db_client_id
#ASTRADB_CLIENT_SECRET = settings.db_client_secret

postgres_client_password = settings.db_client_password



DATABASE_URL = "postgresql://postgres:postgres_client_password@localhost:5432/api"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#def get_session():
#    DATABASE_URL = "postgresql://POSTGRES_CLIENT_USERNAME:POSTGRES_CLIENT_PASSWORD@localhost:5432/api"
#    engine = create_engine(DATABASE_URL)
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
#    return SessionLocal

def get_db():
    dbs = SessionLocal()
    try:
        yield dbs
    finally:
        dbs.close()    



