import asyncio
import random
import smtplib
import string
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from uuid import UUID, uuid4

import jwt
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from core.config import settings
from core.const import DT_FORMAT
from database.dto.user import UserCreateDTO
from database.models.models import (JWT_Token_Blacklist, Users,
                                    Verification_Codes)
from services.base import ServiceBase


class AuthMaster(ServiceBase):

    CODE_LENGTH = 6
    EXPIRE_TIME_MINUTES = 5

    async def send_mailcode(self, email: str, purpose: str = "login") -> dict:

        async with self._db.get_session() as session:
            result = await session.execute(select(Users).where(Users.email == email))
            user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f"Пользователь с email {email!r} не найден")

        if user.is_blocked:
            raise PermissionError("Пользователь заблокирован")

        now = datetime.now(timezone.utc)

        async with self._db.get_session() as session:
            result = await session.execute(
                select(Verification_Codes).where(
                    Verification_Codes.user_id == user.id,
                    Verification_Codes.purpose == purpose,
                    Verification_Codes.is_used.is_(False),
                    Verification_Codes.expires_at > now,
                )
            )
            existing = result.scalar_one_or_none()

        if existing:
            raise ValueError("Активный код уже отправлен, дождитесь его истечения")

        code = "".join(random.choices(string.digits, k=self.CODE_LENGTH))
        expires_at = now + timedelta(minutes=self.EXPIRE_TIME_MINUTES)

        async with self._db.get_session() as session:
            await session.execute(
                insert(Verification_Codes).values(
                    user_id=user.id,
                    code=code,
                    purpose=purpose,
                    expires_at=expires_at,
                    is_used=False,
                )
            )
            await session.commit()

        await self._send_email(email, code)

        return {"send": True, "email": email, "sent_at": now.strftime(DT_FORMAT)}

    async def purge_expired_codes(self) -> dict:

        now = datetime.now(timezone.utc)
        async with self._db.get_session() as session:
            result = await session.execute(
                delete(Verification_Codes).where(Verification_Codes.expires_at <= now)
            )
            await session.commit()
        return {"quantity": result.rowcount, "deleted_at": now.strftime(DT_FORMAT)}

    async def sign_up(
        self,
        email: str,
        phone: str,
        display_name: str,
        role_id: int,
    ) -> dict:

        user_dto = UserCreateDTO(
            email=email,
            phone=phone,
            display_name=display_name,
            role_id=role_id,
            email_verified=False,
        )

        async with self._db.get_session() as session:
            try:
                await session.execute(insert(Users).values(**user_dto.model_dump()))
                await session.commit()
            except IntegrityError:
                raise ValueError(
                    "Пользователь с таким email или телефоном уже существует"
                )

        return await self.send_mailcode(email, purpose="email_verify")

    async def sign_in(self, email: str, code: str) -> dict:

        now = datetime.now(timezone.utc)

        async with self._db.get_session() as session:
            result = await session.execute(select(Users).where(Users.email == email))
            user = result.scalar_one_or_none()

        if not user:
            raise ValueError("Пользователь не найден")

        if user.is_blocked:
            raise PermissionError("Пользователь заблокирован")

        async with self._db.get_session() as session:
            result = await session.execute(
                select(Verification_Codes).where(
                    Verification_Codes.user_id == user.id,
                    Verification_Codes.code == code,
                    Verification_Codes.purpose == "login",
                    Verification_Codes.is_used.is_(False),
                    Verification_Codes.expires_at > now,
                )
            )
            verification = result.scalar_one_or_none()

        if not verification:
            raise ValueError("Неверный или истёкший код")

        async with self._db.get_session() as session:
            await session.execute(
                update(Verification_Codes)
                .where(Verification_Codes.id == verification.id)
                .values(is_used=True)
            )
            await session.execute(
                update(Users).where(Users.id == user.id).values(last_login_time=now)
            )
            await session.commit()

        access_token = self._create_token(user.id, user.role_id, "access")
        refresh_token = self._create_token(user.id, user.role_id, "refresh")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "signed_in_at": now.strftime(DT_FORMAT),
        }

    async def sign_out(self, token: str) -> dict:

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret.get_secret_value(),
                algorithms=[settings.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Токен истёк")
        except jwt.InvalidTokenError:
            raise ValueError("Недействительный токен")

        jti: str | None = payload.get("jti")
        exp: int | None = payload.get("exp")

        if not jti or not exp:
            raise ValueError("Токен не содержит обязательных данных")

        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)

        now = datetime.now(timezone.utc)

        async with self._db.get_session() as session:
            await session.execute(
                insert(JWT_Token_Blacklist).values(
                    jwt_id=jti,
                    expires_at=expires_at,
                )
            )
            await session.commit()

        return {"sign_out": True, "signed_out_at": now.strftime(DT_FORMAT)}

    async def refresh(self, refresh_token: str) -> dict:

        payload = await self._validate_token(refresh_token, expected_type="refresh")

        user_id = UUID(payload["sub"])
        role_id: int = payload["role_id"]

        now = datetime.now(timezone.utc)
        access_token = self._create_token(user_id, role_id, "access")

        return {"access_token": access_token, "refreshed_at": now.strftime(DT_FORMAT)}

    async def verify_token(self, token: str) -> dict:

        return await self._validate_token(token, expected_type="access")

    def _create_token(self, user_id: UUID, role_id: int, token_type: str) -> str:
        now = datetime.now(timezone.utc)

        if token_type == "access":
            expire = now + timedelta(minutes=settings.jwt_access_expire_minutes)
        else:
            expire = now + timedelta(days=settings.jwt_refresh_expire_days)

        payload = {
            "sub": str(user_id),
            "role_id": role_id,
            "type": token_type,
            "jti": str(uuid4()),
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
        }

        return jwt.encode(
            payload,
            settings.jwt_secret.get_secret_value(),
            algorithm=settings.jwt_algorithm,
        )

    async def _validate_token(self, token: str, expected_type: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret.get_secret_value(),
                algorithms=[settings.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Токен истёк")
        except jwt.InvalidTokenError:
            raise ValueError("Недействительный токен")

        if payload.get("type") != expected_type:
            raise ValueError(f"Ожидался {expected_type!r} токен")

        jti: str | None = payload.get("jti")

        async with self._db.get_session() as session:
            result = await session.execute(
                select(JWT_Token_Blacklist).where(JWT_Token_Blacklist.jwt_id == jti)
            )
            if result.scalar_one_or_none():
                raise ValueError("Токен отозван")

        return payload

    async def _send_email(self, to_email: str, code: str) -> None:
        msg = MIMEText(
            f"Ваш код подтверждения: {code}\n"
            f"Код действителен {self.EXPIRE_TIME_MINUTES} минут.",
            "plain",
            "utf-8",
        )
        msg["Subject"] = "Код подтверждения"
        msg["From"] = settings.smtp_from
        msg["To"] = to_email

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._smtp_send, msg.as_string(), to_email)

    def _smtp_send(self, message: str, to_email: str) -> None:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_user, settings.smtp_password.get_secret_value())
            server.sendmail(settings.smtp_from, to_email, message)
