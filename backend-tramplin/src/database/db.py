from contextlib import asynccontextmanager
from typing import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import (Asyn, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from core.config import settings
from core.const import ORJSON_PROPERTIES_MASK


class Database:

    def __init__(
        self,
        conn_url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 10,
        pool_pre_ping: bool = False,
    ):

        self.url = conn_url

        self.__engine: AsyncEngine = create_async_engine(
            url=self.url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=10,
            pool_pre_ping=pool_pre_ping,
            json_serializer=self.orjson_serializer,
            json_deserializer=self.orjson_deserializer,
        )

        self.__session_maker = async_sessionmaker(
            self._engine, expire_on_commit=True, autoflush=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_maker() as session:
            yield session

    async def dispose(self):
        await self.__engine.dispose()

    @staticmethod
    def orjson_serializer(data) -> str:
        return orjson.dumps(data, ORJSON_PROPERTIES_MASK).decode()

    @staticmethod
    def orjson_deserializer(json_data) -> object:
        return orjson.loads(json_data)
