from enum import StrEnum, auto


ENV_FILE_NAME=".env"
ENV_FILE_ENCODING="utf-8"
ENV_NESTED_DELIMETER="__"
DEFAULT_TIMEZONE="Europe/Moscow"


class VerificationMethod(StrEnum):
    EMAIL = auto().lower()
    INN = auto().lower()
    SOCIAL = auto().lower()