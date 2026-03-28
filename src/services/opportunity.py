from sys import stderr
from uuid import UUID

from loguru import logger
from sqlalchemy import delete, func, insert, select, update

from core.types import OpportunityDict
from database.dto.opportunity import (OpportunityDTO, OpportunityEditDTO,
                                      OpportunityFiltersDTO,
                                      OpportunityListWithQuantityDTO, OpportunityCreateDTO)
from database.models.models import Opportunities, Tags, Opportunity_Tags
from services.base import ServiceBase
from utils.funcs import serialize_dict_for_response

logger.add(stderr, format="{time} {level} {message}", level="DEBUG", colorize=True)


class OpportunityMaster(ServiceBase):

    async def get_all_with_filters(
        self,
        filters: OpportunityFiltersDTO,
        page: int = 1,
        page_records_count: int = 10,
    ) -> list[OpportunityDict]:

        filters_list: list = self.__make_filters_list_from_pydantic_model(filters)
        logger.debug(f"fls: {filters_list}")
        async with self._db.get_session() as session:
            try:
                query = select(Opportunities)
                count_query = select(func.count(Opportunities.id))

                if filters_list:
                    query = query.where(*filters_list)
                    count_query = count_query.where(*filters_list)

                count_result = await session.execute(count_query)
                total_count = count_result.scalar_one()

                offset = (page - 1) * page_records_count
                query = (
                    query.offset(offset)
                    .limit(page_records_count)
                    .order_by(Opportunities.publication_date.desc())
                )

                result = await session.execute(query)
                items = result.scalars().all()

                return OpportunityListWithQuantityDTO(
                    opportunities=[
                        OpportunityDTO.model_validate(item, from_attributes=True)
                        for item in items
                    ],
                    quantity=total_count,
                )

            except Exception as e:
                logger.error(e)
                raise

    async def get_one(self, opportunity_id: UUID) -> OpportunityDict | None:

        async with self._db.get_session() as session:

            query = select(Opportunities).where(Opportunities.id == opportunity_id)
            result = await session.execute(query)

            item = result.scalar_one_or_none()
            model = OpportunityDTO.model_validate(item)

            return model.model_dump() if item is not None else None

    async def create_one(self, opportunity_dto: OpportunityCreateDTO) -> OpportunityDict:

        opportunity_data = {
            k: v
            for k, v in opportunity_dto.model_dump(exclude={"tags_data"}).items()
            if v is not None
        }

        async with self._db.get_session() as session:

            stmt = insert(Opportunities).values(**opportunity_data).returning(Opportunities.id)
            result = await session.execute(stmt)
            new_opportunity_id = result.scalar_one()

            tag_ids: list = []
            if opportunity_dto.tags_data:
                for tag in opportunity_dto.tags_data:
                    tag_name = tag.name
                    tag_category = tag.category
                    # Пытаемся найти существующий тег
                    tag_query = select(Tags.id).where(Tags.name == tag_name)
                    tag_result = await session.execute(tag_query)
                    tag_id = tag_result.scalar_one_or_none()

                    if tag_id is None:
                        insert_tag = insert(Tags).values(
                            name=tag_name,
                            category=tag_category or 'skill',
                            is_system=False
                        ).returning(Tags.id)
                        tag_result = await session.execute(insert_tag)
                        tag_id = tag_result.scalar_one()

                    tag_ids.append(tag_id)

                if tag_ids:
                    values = [
                        {"opportunity_id": new_opportunity_id, "tag_id": t_id}
                        for t_id in tag_ids
                    ]
                    insert_links = insert(Opportunity_Tags).values(values)
                    await session.execute(insert_links)

            await session.commit()
            
            response_data = serialize_dict_for_response({
                **opportunity_data,
                "id": new_opportunity_id,
                "tags_data": [t.model_dump() for t in opportunity_dto.tags_data] if opportunity_dto.tags_data else []
            })
            return response_data


    async def edit_one(
        self, opportunity_id: UUID, new_opportunity_dto: OpportunityEditDTO
    ) -> OpportunityDict:

        opportunity_data: OpportunityDict = {
            key: value
            for key, value in new_opportunity_dto.model_dump().items()
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

        return serialize_dict_for_response(opportunity_data)

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

    def __make_filters_list_from_pydantic_model(
        self, filters: OpportunityFiltersDTO
    ) -> list:

        filters_dict: dict = filters.model_dump(exclude_none=True)
        filters_list: list = []

        for field_name, value in filters_dict.items():
            field = getattr(Opportunities, field_name, None)
            if field is not None:
                if value is not None:
                    filters_list.append(field == value)

        return filters_list

    async def add_tag(): ...  ## TODO: с тегами тут доделать
    async def remove_tag(): ...
