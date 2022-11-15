from model import Base
from sqlalchemy import String, Column, Identity, Integer, Text


class invite_message_class(Base):
    __tablename__ = 'invite_message'
    id = Column(Integer, Identity(), primary_key=True)
    invite_message = Column(Text)
    invite_picture = Column(String(200))
    chanel_id = Column(String(200))
    chanel_name = Column(String(200))