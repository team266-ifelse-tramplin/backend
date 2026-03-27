from fastapi import APIRouter
from fastapi import Request

auth_router = APIRouter(prefix="/account", tags=["Account"])

@auth_router.post("/sign_up")
async def sign_up(request: Request):
    ...

@auth_router.post("/sign_in")
async def sign_in(request: Request):
    ...

@auth_router.post("/sign_out")
async def sign_out(request: Request):
    ...

@auth_router.post("/send_email_code")
async def send_email_code(request: Request):
    ...