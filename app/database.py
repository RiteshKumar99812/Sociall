from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from .config import settings
from psycopg2.extras import RealDictCursor

# connection ot the database 
# while True :
#   try : 
#       conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres' , password = 'Riteshjee@99', cursor_factory= RealDictCursor)
#       cursor = conn.cursor()
#       print("Database connection was succesfull")
#       break
#   except Exception as error :
#     print("Connection to the Database failed")
#     print("Error",error)
#     time.sleep(2)

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{quote_plus(settings.database_password)}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL , echo = True)



SessionLocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)
Base = declarative_base()
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally: 
    db.close()