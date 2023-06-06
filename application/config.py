from pydantic import BaseSettings, Field
from functools import lru_cache
from pathlib import Path
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"



class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / 'templates'
    
    #keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    #db_client_username: str = Field(..., env='POSTGRES_CLIENT_USERNAME')
    db_client_password: str = Field(..., env='POSTGRES_CLIENT_PASSWORD')
    secret_key: str = Field(..., env='SECRET_KEY')
    jwt_algorithm: str = Field(default='HS256')

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()         