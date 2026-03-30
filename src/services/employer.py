from uuid import UUID

from sqlalchemy import delete, insert, select, update

from database.dto.applications import (ApplicationDTO,
                                       ApplicationsListWithQuantity)
from database.dto.employer import EmployerCreateDTO, EmployerEditDTO
from database.dto.opportunity import (OpportunityDTO,
                                      OpportunityListWithQuantityDTO)
from database.models.models import Applications, Employers, Opportunities
from services.base import UserServiceBase


class Employer(UserServiceBase):

    __role_id: int = 4

    async def create_employer(self, employer_data: EmployerCreateDTO) -> dict:
        user_created_data: dict = await self.create_user(employer_data.user)
        employer_data_dict = employer_data.model_dump(exclude={"user"})
        async with self._db.get_session() as session:
            query = insert(Employers).values(
                user_id=user_created_data["id"], **employer_data_dict
            )
            await session.execute(query)
            await session.commit()
        return employer_data_dict

    async def edit_employer(
        self, employer_data: EmployerEditDTO, user_id: UUID
    ) -> tuple[dict, dict]:
        employer_data_dict = {
            k: v
            for k, v in employer_data.model_dump(exclude={"user"}).items()
            if v is not None
        }
        async with self._db.get_session() as session:
            query = (
                update(Employers)
                .values(**employer_data_dict)
                .where(Employers.user_id == user_id)
                .execution_options(synchronize_session=False)
            )
            await session.execute(query)
            await session.commit()
            if employer_data.user:
                updated_user_data = await self.edit_user(user_id, employer_data.user)

        return employer_data_dict, updated_user_data

    async def delete_employer(self, user_id: UUID) -> None:
        async with self._db.get_session() as session:
            await session.execute(delete(Employers).where(Employers.user_id == user_id))
            await self.delete_user(user_id)
            await session.commit()

    async def get_employer_opportunities(
        self, user_id: UUID
    ) -> OpportunityListWithQuantityDTO:
        async with self._db.get_session() as session:
            company_id_result = await session.execute(
                select(Employers.company_id).where(Employers.user_id == user_id)
            )
            company_id = company_id_result.scalar_one()

            result = await session.execute(
                select(Opportunities).where(Opportunities.company_id == company_id)
            )
            items = result.scalars().all()

            return OpportunityListWithQuantityDTO(
                opportunities=[
                    OpportunityDTO.model_validate(item, from_attributes=True)
                    for item in items
                ],
                quantity=len(items),
            )

    async def get_applications_by_opportunity_id(
        self, opportunity_id: UUID
    ) -> ApplicationsListWithQuantity:
        async with self._db.get_session() as session:
            result = await session.execute(
                select(Applications).where(
                    Applications.opportunity_id == opportunity_id
                )
            )
            items = result.scalars().all()

            return ApplicationsListWithQuantity(
                applications=[
                    ApplicationDTO.model_validate(item, from_attributes=True)
                    for item in items
                ],
                quantity=len(items),
            )
