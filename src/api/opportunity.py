from datetime import datetime, timezone
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, Response
from loguru import logger

from database.dto.opportunity import (OpportunityCreateDTO, OpportunityEditDTO,
                                      OpportunityFiltersDTO)
from services.opportunity import OpportunityMaster
from utils.funcs import convert_uuid_to_str_in_data

opportunity_router = APIRouter(prefix="/opportunities", tags=["Opportunity"])


@opportunity_router.get(
    "/get_all", description="Получение всех возможностей (с опциональной фильтрацией)"
)
async def get_all_opps(request: Request, filters: OpportunityFiltersDTO = Depends()):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        result = await op_master.get_all_with_filters(filters)
        return JSONResponse(
            content={
                "quantity": result.quantity,
                "data": convert_uuid_to_str_in_data(
                    [item.model_dump() for item in result.opportunities]
                ),
            },
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@opportunity_router.get(
    "/get_one", description="Получение конкретной возможности по ID"
)
async def get_one(request: Request, opportunity_id: UUID | str):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        result = await op_master.get_one(opportunity_id)
        return JSONResponse(
            content=convert_uuid_to_str_in_data(result), status_code=HTTPStatus.OK
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@opportunity_router.post("/create_one", description="Создание возможности")
async def create_one(request: Request, opportunity_dto: OpportunityCreateDTO):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        result = await op_master.create_one(opportunity_dto)
        with_str_uuid_data = convert_uuid_to_str_in_data(result)
        
        return JSONResponse(
            content={

                "data": with_str_uuid_data,
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


@opportunity_router.put("/edit_one", description="Изменение данных возможности")
async def edit_one(
    request: Request, opportunity_id: UUID, new_opporuntity_dto: OpportunityEditDTO
):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        result = await op_master.edit_one(opportunity_id, new_opporuntity_dto)
        return JSONResponse(
            content={
                "new_data": result,
                "updated_at": datetime.now(tz=timezone.utc).isoformat(
                    sep=" ", timespec="seconds"
                ),
            },
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@opportunity_router.delete("/delete_one", description="Удаление возможности")
async def delete_one(request: Request, opportunity_id: UUID):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        await op_master.delete_one(opportunity_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@opportunity_router.delete(
    "/delete_all_by_company_id",
    description="Удаление одной/нескольких/всех возможностей одной компании",
)
async def delete_all_by_id(request: Request, company_id: UUID):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        total_deleted = await op_master.delete_all_by_id(company_id)
        return JSONResponse(
            content={
                "quantity": total_deleted,
                "deleted_at": datetime.now(tz=timezone.utc).isoformat(
                    sep=" ", timespec="seconds"
                ),
            },
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )
