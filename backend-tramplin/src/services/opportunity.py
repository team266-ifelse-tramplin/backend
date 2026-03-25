from uuid import UUID

from base import ServiceBase
from sqlalchemy import delete, func, insert, select, update

from core.types import OpportunityDict, OpportunityListWithQuantity
from database.dto.opportunity import OpportunityDTO, OpportunityEditDTO
from database.models.models import Opportunities


class OpportunityMaster(ServiceBase):

    async def get_all_with_filters(
        self, filters: list, page: int = 1, page_records_count: int = 10
    ) -> OpportunityListWithQuantity:

        async with self._db.get_session() as session:

            count_result = await session.execute(select(func.count(Opportunities.id)))
            total_count = count_result.scalar_one()
            offset = (page - 1) * page_records_count
            query = (
                select(Opportunities)
                .where(*filters)
                .offset(offset)
                .limit(page_records_count)
            )
            result = await session.execute(query)
            items = result.mappings().all()

            return [OpportunityDTO.model_validate(item) for item in items], total_count

    async def get_one(self, opportunity_id: UUID) -> OpportunityDict | None:

        async with self._db.get_session() as session:

            query = select(Opportunities).where(Opportunities.id == opportunity_id)
            result = await session.execute(query)

            item = result.scalar_one_or_none()

            return OpportunityDTO.model_validate(item) if item is not None else None

    async def create_one(self, opportunity_dto: OpportunityDTO) -> OpportunityDict:

        opportunity_data: OpportunityDict = opportunity_dto.model_dump()
        async with self._db.get_session() as session:

            query = insert(Opportunities).values(**opportunity_data)
            await session.execute(query)
            await session.commit()

        return opportunity_data

    async def edit_one(
        self, opportunity_id: UUID, new_opportunity_dto: OpportunityEditDTO
    ) -> OpportunityDict:

        opportunity_data: OpportunityDict = {
            key: value
            for key, value in new_opportunity_dto.model_dump()
            if value is not None
        }

        async with self._db.get_session() as session:
            await session.execute(
                update(Opportunities)
                .where(Opportunities.id == opportunity_id)
                .values(**opportunity_data)
                .execution_options(synchronize_session=False)
            )
            await session.commit()

        return opportunity_data

    async def delete_one(self, opportunity_id: UUID) -> None:
        async with self._db.get_session() as session:
            await session.execute(
                delete(Opportunities).where(Opportunities.id == opportunity_id)
            )
            await session.commit()

    async def delete_all_by_id(self, company_id: UUID) -> int:
        async with self._db.get_session() as session:
            count_result = await session.execute(
                select(func.count(Opportunities.id)).where(
                    Opportunities.company_id == company_id
                )
            )
            total_count = count_result.scalar_one()

            await session.execute(
                delete(Opportunities).where(Opportunities.company_id == company_id)
            )
            await session.commit()

            return total_count

    async def add_tag(): ...  ## TODO: с тегами тут доделать
    async def remove_tag(): ...
