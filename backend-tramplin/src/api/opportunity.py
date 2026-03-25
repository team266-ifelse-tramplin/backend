from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from database.dto.opportunity import OpportunityFiltersDTO
from services.opportunity import OpportunityMaster

opportunity_router = APIRouter("opportunities")


@opportunity_router.get(
    "/get_all", description="Получение всех возможностей (с опциональной фильтрацией)"
)
async def get_all_opps(request: Request, filters: OpportunityFiltersDTO = Depends()):
    op_master: OpportunityMaster = request.app.state.op_master
    try:
        result = await op_master.get_all_with_filters(filters)
        return JSONResponse(
            content={"quantity": result[1], "data": result[0]},
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(content={"error": e}, status_code=HTTPStatus.BAD_REQUEST)
