import os
from sqlalchemy.ext.declarative import declarative_base

def getDeclartiveBase():
    global Base
    if Base == None:
        Base = declarative_base()
    return Base

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED_APPS = [
    "item",
    "variant"
]

Base = None

ADDRESS="0.0.0.0"
AUTORELOAD = True
PORT=8888
DEBUG = True

DATABASES = {
   "itemfeed": {
       "type": "mongo",
       "username": "",
       "password": "",
       "database": "itemfeed",
       "host": ["127.0.0.1"],
       "port": [27017],
       "replica_set": ""
   },
   "itemandvariant": {
       "type": "postgresql",
       "username": "darshanms",
       "password": "",
       "database": "itemandvariant",
       "host": "127.0.0.1",
       "port": 5432
   }
}

KAFKA_SERVERS = ["127.0.0.1:9092"]
