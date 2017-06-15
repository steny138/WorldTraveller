from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID,JSON
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import uuid
import sqlalchemy.types as types
import settings



DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)

# class UUID(types.TypeEngine):
#     def get_col_spec(self):
#         return "uuid"

#     def bind_processor(self, dialect):
#         def process(value):
#             return value
#         return process

#     def result_processor(self, dialect):
#         def process(value):
#             return value
#         return process

class WorldViews(DeclarativeBase):
    """docstring for WorldViews"""
    
    __tablename__ = 'WorldViews'

    viewid = Column(UUID(as_uuid=True), primary_key= True)
    name = Column(String, nullable= True)
    location = Column(String, nullable= True)
    en_name = Column(String, nullable= True)
    address = Column(String, nullable= True)
    cover = Column(String, nullable= True)
    rate = Column(String, nullable= True)
    comments = Column(String, nullable= True)
    outer_key = Column(String, nullable= True)
    contact = Column(String, nullable= True)
    description = Column(String, nullable= True)
    lat = Column(String, nullable= True)
    lng = Column(String, nullable= True)
    homepage = Column(String, nullable= True)
    business_hours = Column(String, nullable= True)
        