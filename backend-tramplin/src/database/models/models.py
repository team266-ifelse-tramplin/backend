from datetime import datetime
from uuid import uuid4

from sqlalchemy import (UUID, Boolean, CheckConstraint, DateTime, Enum,
                        ForeignKey, Integer, Numeric, PrimaryKeyConstraint,
                        String, Text, UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.config import settings
from core.const import VerificationMethod
from database.models.base import Base

## TODO: relationship подумать


class Users(Base):

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    phone: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_login_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Verification_Codes(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    purpose: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  ## "login", "email_verify"
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )


class JWT_Token_Blacklist(Base):
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    jwt_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )


class Roles(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False
    )  # admin, guest, applicant, employer


class Permissions(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    permission: Mapped[str] = mapped_column(String(10), nullable=False)

    __table_args__ = (
        UniqueConstraint("resource", "permission", name="uq_resource_permission"),
    )


class Role_Permissions(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("role_id", "permission_id"),)


class Applicants(Base):
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    university: Mapped[str] = mapped_column(String(255))
    graduation_year: Mapped[int] = mapped_column(Integer)
    current_education_year: Mapped[int] = mapped_column(Integer)
    about: Mapped[str] = mapped_column(String(255))

    __table_args__ = (
        CheckConstraint(
            "graduation_year >= EXTRACT(YEAR FROM CURRENT_DATE) AND graduation_year <= EXTRACT(YEAR FROM CURRENT_DATE) + 6",
            name="check_graduation_year_range",
        ),
        CheckConstraint(
            "current_education_year <= graduation_year AND current_education_year >= graduation_year - 6",
            name="check_education_year_range",
        ),
    )


class User_Documents(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    file_name: Mapped[str] = mapped_column(String(255))
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default=settings.default_file_type
    )
    visibility: Mapped[str] = mapped_column(String(20), default="public")
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_draft: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "visibility IN ('public', 'connections', 'private')",
            name="check_visibility_valid",
        ),
        CheckConstraint(
            "(doc_type = 'resume' AND is_draft IS NOT NULL) OR (doc_type = 'portfolio' AND is_draft = false)",
            name="check_draft_only_for_resume",
        ),
    )


class Companies(Base):
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text)
    website: Mapped[str] = mapped_column(Text)
    industry: Mapped[str] = mapped_column(String(100))
    staff_size: Mapped[str] = mapped_column(String(10))
    location_city: Mapped[str] = mapped_column(String(100))
    location_address: Mapped[str] = mapped_column(Text)
    logo_url: Mapped[str] = mapped_column(Text)
    social_links: Mapped[dict] = mapped_column(JSONB, default=dict)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_method: Mapped[str] = mapped_column(Enum(VerificationMethod))
    verification_details: Mapped[str] = mapped_column(JSONB, default=dict)
    verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    verified_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        nullable=False,
    )


class Employers(Base):
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    position: Mapped[str] = mapped_column(String(100))
    # is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )


class Opportunities(Base):
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", onupdate="CASCADE"), nullable=False
    )
    opportunity_type: Mapped[str] = mapped_column(
        String(30), nullable=False, name="type"
    )
    work_format: Mapped[str] = mapped_column(String(30))
    employment: Mapped[str] = mapped_column(String(10))
    level: Mapped[str] = mapped_column(String(10))

    tags: Mapped[list["Tags"]] = relationship(
        secondary="opportunity_tags",
        back_populates="opportunities",
        lazy="selectin",
        viewonly=False,
    )

    location: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Numeric(10, 8))
    longitude: Mapped[float] = mapped_column(Numeric(11, 8))
    salary_from: Mapped[int] = mapped_column(Integer)
    salary_to: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3))
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    contact_info: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )

    __table_args__ = (
        CheckConstraint(
            "type IN ('vacancy', 'internship', 'mentoring', 'event')",
            name="check_opportunity_type_valid",
        ),
        CheckConstraint(
            "work_format IN ('office', 'hybrid', 'remote')",
            name="check_work_format_valid",
        ),
        CheckConstraint(
            "status IN ('active', 'closed', 'draft', 'pending_moderation')",
            name="check_status_valid",
        ),
        CheckConstraint("salary_from <= salary_to", name="check_valid_salary_range"),
        CheckConstraint(
            "employment IN ('full', 'partial')", name="check_employment_valid"
        ),
        CheckConstraint(
            "level IN ('intern', 'junior', 'middle', 'senior')",
            name="check_level_valid",
        ),
    )


class Tags(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50))  # skill, level, employment_type
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )

    opportunities: Mapped[list["Opportunities"]] = relationship(
        secondary="opportunity_tags", back_populates="tags", lazy="selectin"
    )

    __table_args__ = (
        CheckConstraint(
            "category IN ('skill', 'level', 'employment_type')",
            name="check_tag_category_valid",
        ),
    )


class Opportunity_Tags(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    opportunity_id: Mapped[UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE")
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )


class Curators(Base):
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    university: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )


class Applications(Base):

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    opportunity_id: Mapped[UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False
    )
    applicant_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="pending")
    cover_letter: Mapped[str] = mapped_column(Text)
    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        onupdate=lambda: datetime.now(settings.default_timezone),
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected', 'reserved')",
            name="check_application_status_valid",
        ),
        UniqueConstraint(
            "opportunity_id", "applicant_id", name="unique_application_per_opportunity"
        ),
    )


class Favorites(Base):

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    opportunity_id: Mapped[UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )

    __table_args__ = (
        UniqueConstraint("user_id", "opportunity_id", name="unique_favorite_per_user"),
    )


class Connections(Base):

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=text("get_random_uuid()")
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # тот, кто отправил заявку на добавление
    friend_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # тот, кто полуичл заявку на добавление
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(settings.default_timezone)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(settings.default_timezone),
        onupdate=lambda: datetime.now(settings.default_timezone),
    )

    __table_args__ = (
        CheckConstraint("user_id != friend_id", name="check_not_self_connection"),
        CheckConstraint(
            "status IN ('pending', 'accepted')", name="check_connection_status_valid"
        ),
        UniqueConstraint("user_id", "friend_id", name="unique_connection"),
    )
