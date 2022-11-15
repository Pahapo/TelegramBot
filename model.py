from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Identity, Integer, Text


metadata = MetaData()
Base = declarative_base()


class invite_message_class(Base):
    __tablename__ = 'invite_message'
    id = Column(Integer, Identity(), primary_key=True)
    invite_message = Column(Text)
    invite_picture = Column(String(200))
    chanel_id = Column(String(200))
    chanel_name = Column(String(200))


