from fastapi import APIRouter
from core.const import API_URL
from opportunity import opportunity_router



api_router = APIRouter(API_URL)

api_router.include_router(opportunity_router)