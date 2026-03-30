from fastapi import APIRouter

from api.auth import auth_router
from api.favorites import favorites_router
from api.opportunity import opportunity_router
from api.users import user_router
from core.const import API_URL

api_main_router = APIRouter(prefix=API_URL)

api_main_router.include_router(opportunity_router)
api_main_router.include_router(auth_router)
api_main_router.include_router(user_router)
api_main_router.include_router(favorites_router)
