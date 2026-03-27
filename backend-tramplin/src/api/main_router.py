from fastapi import APIRouter

from api.opportunity import opportunity_router
from core.const import API_URL

api_main_router = APIRouter(prefix=API_URL)

api_main_router.include_router(opportunity_router)
