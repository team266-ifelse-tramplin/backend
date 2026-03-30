from datetime import datetime, timezone
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from database.dto.favorites import FavoriteAddDTO
from services.favorites import FavoriteMaster
from utils.funcs import convert_uuid_to_str_in_data

favorites_router = APIRouter(prefix="/Favorites", tags=["Favorites"])


@favorites_router.get(
    "/get_all", description="Получение всех избранных возможностей пользователя"
)
async def get_all(request: Request, user_id: UUID):
    Favorite: FavoriteMaster = request.app.state.Favorite
    try:
        result = await Favorite.get_all(user_id)
        return JSONResponse(
            content={
                "quantity": result.quantity,
                "data": convert_uuid_to_str_in_data(
                    [item.model_dump() for item in result.Favorites]
                ),
            },
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@favorites_router.post("/add", description="Добавление возможности в избранное")
async def add(request: Request, Favorite_dto: FavoriteAddDTO):
    Favorite: FavoriteMaster = request.app.state.Favorite
    try:
        result = await Favorite.add(Favorite_dto)
        return JSONResponse(
            content={
                "data": convert_uuid_to_str_in_data(result),
                "created_at": datetime.now(tz=timezone.utc).isoformat(
                    sep=" ", timespec="seconds"
                ),
            },
            status_code=HTTPStatus.CREATED,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@favorites_router.delete("/remove", description="Удаление возможности из избранного")
async def remove(request: Request, user_id: UUID, opportunity_id: UUID):
    Favorite: FavoriteMaster = request.app.state.Favorite
    try:
        await Favorite.remove(user_id, opportunity_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )
