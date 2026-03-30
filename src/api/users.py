from datetime import datetime, timezone
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from database.dto.applicants import ApplicantCreateDTO, ApplicantEditDTO
from database.dto.applications import ApplicationCreateDTO
from database.dto.employer import EmployerCreateDTO, EmployerEditDTO
from services.applicant import Applicant
from services.employer import Employer
from utils.funcs import convert_uuid_to_str_in_data

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/create_applicant", description="Создание аппликанта")
async def create_applicant(request: Request, applicant_dto: ApplicantCreateDTO):
    applicant: Applicant = request.app.state.applicant
    try:
        result = await applicant.create_applicant(applicant_dto)
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


@user_router.put("/edit_applicant", description="Изменение данных аппликанта")
async def edit_applicant(
    request: Request, user_id: UUID, applicant_dto: ApplicantEditDTO
):
    applicant: Applicant = request.app.state.applicant
    try:
        applicant_data, user_data = await applicant.edit_applicant_data(
            applicant_dto, user_id
        )
        return JSONResponse(
            content={
                "new_data": convert_uuid_to_str_in_data(
                    {**applicant_data, **user_data}
                ),
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


@user_router.delete("/delete_applicant", description="Удаление аппликанта")
async def delete_applicant(request: Request, user_id: UUID):
    applicant: Applicant = request.app.state.applicant
    try:
        await applicant.delete_applicant(user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@user_router.post("/make_application", description="Подача заявки на возможность")
async def make_application(request: Request, application_dto: ApplicationCreateDTO):
    applicant: Applicant = request.app.state.applicant
    try:
        result = await applicant.make_application(application_dto)
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


@user_router.get(
    "/get_all_applications", description="Получение всех заявок аппликанта"
)
async def get_all_applications(request: Request, user_id: UUID):
    applicant: Applicant = request.app.state.applicant
    try:
        result = await applicant.get_all_applications(user_id)
        return JSONResponse(
            content={
                "quantity": result.quantity,
                "data": convert_uuid_to_str_in_data(
                    [item.model_dump() for item in result.applications]
                ),
            },
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@user_router.post("/create_employer", description="Создание работодателя")
async def create_employer(request: Request, employer_dto: EmployerCreateDTO):
    employer: Employer = request.app.state.employer
    try:
        result = await employer.create_employer(employer_dto)
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


@user_router.put("/edit_employer", description="Изменение данных работодателя")
async def edit_employer(request: Request, user_id: UUID, employer_dto: EmployerEditDTO):
    employer: Employer = request.app.state.employer
    try:
        employer_data, user_data = await employer.edit_employer(employer_dto, user_id)
        return JSONResponse(
            content={
                "new_data": convert_uuid_to_str_in_data({**employer_data, **user_data}),
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


@user_router.delete("/delete_employer", description="Удаление работодателя")
async def delete_employer(request: Request, user_id: UUID):
    employer: Employer = request.app.state.employer
    try:
        await employer.delete_employer(user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )


@user_router.get(
    "/get_employer_opportunities",
    description="Получение всех возможностей работодателя",
)
async def get_employer_opportunities(request: Request, user_id: UUID):
    employer: Employer = request.app.state.employer
    try:
        result = await employer.get_employer_opportunities(user_id)
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


@user_router.get(
    "/get_applications_by_opportunity",
    description="Получение всех заявок по возможности",
)
async def get_applications_by_opportunity(request: Request, opportunity_id: UUID):
    employer: Employer = request.app.state.employer
    try:
        result = await employer.get_applications_by_opportunity_id(opportunity_id)
        return JSONResponse(
            content={
                "quantity": result.quantity,
                "data": convert_uuid_to_str_in_data(
                    [item.model_dump() for item in result.applications]
                ),
            },
            status_code=HTTPStatus.OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"type": str(e.__class__), "message": str(e)},
            status_code=HTTPStatus.BAD_REQUEST,
        )
