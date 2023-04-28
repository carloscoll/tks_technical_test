from datetime import datetime

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import MetaData, Column, Integer, DateTime
from app.core.db.session import get_db_conn

metadata = MetaData()


@as_declarative(bind=get_db_conn())
class Base:
    id = Column(Integer, primary_key=True, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
