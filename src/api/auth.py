from http import HTTPStatus

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from database.dto.auth import (RefreshDTO, SendMailcodeDTO, SignInDTO,
                               SignOutDTO, SignUpDTO)
from services.auth import AuthMaster

auth_router = APIRouter(prefix="/account", tags=["Account"])


@auth_router.post("/sign_up", description="Регистрация нового пользователя")
async def sign_up(request: Request, sign_up_dto: SignUpDTO):
    auth: AuthMaster = request.app.state.auth
    try:
        result = await auth.sign_up(
            email=sign_up_dto.email,
            phone=sign_up_dto.phone,
            display_name=sign_up_dto.display_name,
            role_id=sign_up_dto.role_id,
        )
        return JSONResponse(content=result, status_code=HTTPStatus.CREATED)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@auth_router.post("/sign_in", description="Вход по email + OTP-коду")
async def sign_in(request: Request, sign_in_dto: SignInDTO):
    auth: AuthMaster = request.app.state.auth
    try:
        result = await auth.sign_in(
            email=sign_in_dto.email,
            code=sign_in_dto.code,
        )
        return JSONResponse(content=result, status_code=HTTPStatus.OK)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@auth_router.post("/sign_out", description="Выход — инвалидация токена")
async def sign_out(request: Request, sign_out_dto: SignOutDTO):
    auth: AuthMaster = request.app.state.auth
    try:
        result = await auth.sign_out(token=sign_out_dto.token)
        return JSONResponse(content=result, status_code=HTTPStatus.OK)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@auth_router.post("/send_email_code", description="Отправка OTP-кода на email")
async def send_email_code(request: Request, mailcode_dto: SendMailcodeDTO):
    auth: AuthMaster = request.app.state.auth
    try:
        result = await auth.send_mailcode(
            email=mailcode_dto.email,
            purpose=mailcode_dto.purpose,
        )
        return JSONResponse(content=result, status_code=HTTPStatus.OK)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@auth_router.post(
    "/refresh", description="Обновление access-токена через refresh-токен"
)
async def refresh(request: Request, refresh_dto: RefreshDTO):
    auth: AuthMaster = request.app.state.auth
    try:
        result = await auth.refresh(refresh_token=refresh_dto.refresh_token)
        return JSONResponse(content=result, status_code=HTTPStatus.OK)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@auth_router.delete(
    "/purge_expired_codes",
    description="Удаление всех истёкших OTP-кодов из таблицы",
)
async def purge_expired_codes(request: Request):
    auth: AuthMaster = request.app.state.auth
    try:
        result = await auth.purge_expired_codes()
        return JSONResponse(content=result, status_code=HTTPStatus.OK)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )
