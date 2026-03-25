from fastapi import APIRouter, Depends
from fastapi import Request
from database.dto.opportunity import OpportunityFiltersDTO


opportunity_router = APIRouter(
    "opportunities"
)

@opportunity_router.get("/get_all", description="Получение всех возможностей (с опциональной фильтрацией)")
async def get_all_opps(request: Request, filters: OpportunityFiltersDTO = Depends()):
    ...