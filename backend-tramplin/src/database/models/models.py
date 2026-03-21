from models.base import Base
from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, text, ForeignKey, Boolean, DateTime, UniqueConstraint, PrimaryKeyConstraint
from core.config import settings
from datetime import datetime
from src.database.models.models import Opportunities


## TODO: relationship подумать

class Users(Base):

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()"))
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(settings.default_timezone), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_login_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Verification_Codes(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    purpose: Mapped[str] = mapped_column(String(20), nullable=False) ## "login", "email_verify"
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(settings.default_timezone), nullable=False)


class JWT_Token_Blacklist(Base):
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()"))
    jwt_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(settings.default_timezone), nullable=False)


class Roles(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), unique=True, nullable=False) # admin, guest, applicant, employer

class Permissions(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    permission: Mapped[str] = mapped_column(String(10), nullable=False)

    __table_args__ = (
        UniqueConstraint('resource', 'permission', name='uq_resource_permission'),
    )


class Role_Permissions(Base):
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("role_id", "permission_id"),
    )

class Applicants(Base): ...
class Companies(Base): ...
class Employers(Base): ...
class Admins(Base): ...
class Opportunities(Base): ...
class Tags(Base): ...
class Opportunity_Tags(Base): ...
class Applications(Base): ...
class Favorites(Base): ...
class Connections(Base): ...

