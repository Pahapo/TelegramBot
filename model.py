from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from database_bot import invite_message_class


metadata = MetaData()
Base = declarative_base()


