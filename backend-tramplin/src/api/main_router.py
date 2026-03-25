from fastapi import APIRouter
from opportunity import opportunity_router

from core.const import API_URL

api_router = APIRouter(API_URL)

api_router.include_router(opportunity_router)
