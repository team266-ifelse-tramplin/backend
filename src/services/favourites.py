from uuid import UUID

from sqlalchemy import delete, insert, select

from database.dto.favourites import (FavouriteAddDTO, FavouriteDTO,
                                     FavouritesListWithQuantity)
from database.models.models import Favorites
from services.base import ServiceBase


class FavouriteMaster(ServiceBase):

    async def get_all(self, user_id: UUID) -> FavouritesListWithQuantity:
        async with self._db.get_session() as session:
            query = select(Favorites).where(Favorites.user_id == user_id)
            result = await session.execute(query)
            items = result.scalars().all()

            return FavouritesListWithQuantity(
                favourites=[FavouriteDTO.model_validate(item, from_attributes=True) for item in items],
                quantity=len(items)
            )

    async def add(self, favourite_data: FavouriteAddDTO) -> dict:
        favourite_data_dict = favourite_data.model_dump()
        async with self._db.get_session() as session:
            query = insert(Favorites).values(**favourite_data_dict)
            await session.execute(query)
            await session.commit()
        return favourite_data_dict

    async def remove(self, user_id: UUID, opportunity_id: UUID) -> None:
        async with self._db.get_session() as session:
            query = delete(Favorites).where(
                Favorites.user_id == user_id,
                Favorites.opportunity_id == opportunity_id
            )
            await session.execute(query)
            await session.commit()
