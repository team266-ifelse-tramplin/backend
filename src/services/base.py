from abc import ABC
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from core.config import settings
from core.const import ROLES
from database.db import Database
from database.dto.user import UserCreateDTO, UserEditDTO
from database.models.models import Roles, Users


class ServiceBase(ABC):

    _db = Database(settings.db_conn_link)


class UserServiceBase(ServiceBase):

    __role_id: int = None

    async def create_user(self, user_data: UserCreateDTO) -> dict:

        user_data_dict: dict = user_data.model_dump()

        async with self._db.get_session() as session:
            query = insert(Users).values(**user_data_dict)
            await session.execute(query)
            await session.commit()

        return user_data_dict

    async def edit_user(self, user_id: UUID, new_user_data: UserEditDTO) -> dict:

        new_user_data_dict: dict = {
            key: value for key, value in new_user_data.model_dump() if value is not None
        }

        async with self._db.get_session() as session:
            query = (
                update(Users)
                .where(Users.id == user_id)
                .values(**new_user_data_dict)
                .execution_options(synchronize_session=False)
            )
            await session.execute(query)
            await session.commit()

        return new_user_data_dict

    async def delete_user(self, user_id: UUID) -> None:
        async with self._db.get_session() as session:
            await session.execute(delete(Users).where(Users.id == user_id))
            await session.commit()

    @classmethod
    async def get_perms(cls):
        async with cls._db.get_session() as session:
            await session.execute(
                select(Roles.permissions).where(Roles.id == cls.__role_id)
            )

    @property
    def role(self) -> int:
        return ROLES[self.__role_id]
