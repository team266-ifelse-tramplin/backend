from abc import ABC, abstractmethod

from core.config import settings
from database.db import Database
from database.dto.user import UserCreateDTO, UserEditDTO
from uuid import UUID
from core.const import ROLES

class ServiceBase(ABC):

    _db = Database(settings.db_conn_link)


# class UserServiceBase(ABC, ServiceBase):

#     __role_id: int = None
    
    # @abstractmethod
    # async def create_user(self, user_data: UserCreateDTO):
    #     pass

    # @abstractmethod
    # async def edit_user(self, user_id: UUID, new_user_data: UserEditDTO):
    #     pass

    # @abstractmethod
    # async def delete_user(self, user_id: UUID):
    #     pass

    # @abstractmethod
    # async def get_perms(self, user_id: UUID):
    #     pass

    # @property
    # def role(self) -> int:
    #     return ROLES[self.__role_id]




