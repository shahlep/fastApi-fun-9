from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# step 1 - create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# step 2 - bind engine with session
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# step 3 - define declarative base for describing database tables
Base = declarative_base()


