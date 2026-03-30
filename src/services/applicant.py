from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update

from database.dto.applicants import ApplicantCreateDTO, ApplicantEditDTO
from database.dto.user import UserCreateDTO
from database.models.models import Applicants, Applications
from services.base import UserServiceBase
from src.database.dto.applications import (ApplicationCreateDTO,
                                           ApplicationDTO,
                                           ApplicationsListWithQuantity)


class Applicant(UserServiceBase):

    __role_id: int = 2

    async def create_applicant(self, user_data: ApplicantCreateDTO) -> dict[str, Any]:
        user_created_data: dict = await self.create_user(user_data.user)
        applicant_data_dict = user_data.model_dump(exclude={"user"})
        async with self._db.get_session() as session:
            query = insert(Applicants).values(
                user_id=user_created_data["id"], **applicant_data_dict
            )
            await session.execute(query)
            await session.commit()
        return applicant_data_dict

    async def make_application(
        self, application_data: ApplicationCreateDTO
    ) -> dict[str, Any]:
        application_data_dict = application_data.model_dump()
        async with self._db.get_session() as session:
            query = insert(Applications).values(**application_data_dict)
            await session.execute(query)
            await session.commit()
        return application_data_dict

    async def delete_applicant(self, user_id: UUID) -> None:
        async with self._db.get_session() as session:
            await session.execute(Applicants).where(Applicants.user_id == user_id)
            await self.delete_user(user_id)
            await session.commit()

    async def edit_applicant_data(
        self, applicant_new_data: ApplicantEditDTO, user_id: UUID
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        applicant_new_data_dict = applicant_new_data.model_dump(exclude=["user"])
        async with self._db.get_session() as session:
            query = (
                update(Applicants)
                .values(**applicant_new_data_dict)
                .where(Applicants.user_id == user_id)
                .execution_options(synchronize_session=False)
            )
            await session.execute(query)
            await session.commit()
            if applicant_new_data.user:
                updated_user_data = await self.edit_user(
                    user_id, applicant_new_data.user
                )

        return applicant_new_data_dict, updated_user_data

    async def get_all_applications(self, user_id: UUID) -> ApplicationsListWithQuantity:
        async with self._db.get_session() as session:
            query = select(Applications).where(Applications.applicant_id == user_id)
            result = await session.execute(query)
            items = result.scalars().all()

            return ApplicationsListWithQuantity(
                applications=[
                    ApplicationDTO.model_validate(item, from_attributes=True)
                    for item in items
                ],
                quantity=len(items),
            )
