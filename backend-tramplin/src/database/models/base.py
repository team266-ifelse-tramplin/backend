from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
