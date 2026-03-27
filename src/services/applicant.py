# from services.base import UserServiceBase
# from database.dto.user import UserCreateDTO, UserEditDTO
# from database.models.models import Users
# from sqlalchemy import insert, update
# from uuid import UUID



# class Applicant(UserServiceBase):

#     __role_id: int = 2

#     async def create_user(self, user_data: UserCreateDTO) -> dict:

#         user_data_dict: dict = user_data.model_dump()

#         async with self._db.get_session() as session:
#             query = insert(Users).values(**user_data_dict)
#             await session.execute(query)
#             await session.commit()

#         return user_data_dict
    
#     async def edit_user(self, user_id: UUID, new_user_data: UserEditDTO) -> dict:

#         new_user_data_dict: dict = {key: value
#             for key, value in new_user_data.model_dump()
#             if value is not None
#         }

#         async with self._db.get_session() as session:
#             query = update(Users).where(Users.id == user_id).values(**new_user_data_dict).execution_options(synchronize_session=False)
#             await session.execute(query)
#             await session.commit()
        
#         return new_user_data_dict
    
#     async def delete_user(self, user_id: UUID):
#         ...
        