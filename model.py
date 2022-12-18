from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Identity, Integer, Text, VARCHAR


metadata = MetaData()
Base = declarative_base()


class invite_message_class(Base):
    __tablename__ = 'invite_message'
    id = Column(Integer, Identity(), primary_key=True)
    invite_message = Column(Text)
    invite_picture = Column(String(200))
    chanel_id = Column(String(200))
    chanel_name = Column(String(200))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Identity(), primary_key=True)
    user_id = Column(VARCHAR(200), unique=True, nullable=False)

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'


