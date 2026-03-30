from uuid import UUID

from sqlalchemy import delete, insert, select

from database.dto.favorites import (FavoriteAddDTO, FavoriteDTO,
                                    FavoritesListWithQuantity)
from database.models.models import Favorites
from services.base import ServiceBase


class FavoriteMaster(ServiceBase):

    async def get_all(self, user_id: UUID) -> FavoritesListWithQuantity:
        async with self._db.get_session() as session:
            query = select(Favorites).where(Favorites.user_id == user_id)
            result = await session.execute(query)
            items = result.scalars().all()

            return FavoritesListWithQuantity(
                Favorites=[
                    FavoriteDTO.model_validate(item, from_attributes=True)
                    for item in items
                ],
                quantity=len(items),
            )

    async def add(self, favorite_data: FavoriteAddDTO) -> dict:
        Favorite_data_dict = favorite_data.model_dump()
        async with self._db.get_session() as session:
            query = insert(Favorites).values(**Favorite_data_dict)
            await session.execute(query)
            await session.commit()
        return Favorite_data_dict

    async def remove(self, user_id: UUID, opportunity_id: UUID) -> None:
        async with self._db.get_session() as session:
            query = delete(Favorites).where(
                Favorites.user_id == user_id, Favorites.opportunity_id == opportunity_id
            )
            await session.execute(query)
            await session.commit()
