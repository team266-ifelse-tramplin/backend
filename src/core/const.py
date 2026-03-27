from enum import StrEnum, auto

import orjson

ENV_FILE_NAME = "../.env"
ENV_FILE_ENCODING = "utf-8"
ENV_NESTED_DELIMETER = "__"

DEFAULT_TIMEZONE = "Europe/Moscow"

ORJSON_PROPERTIES_MASK = (
    orjson.OPT_INDENT_2
    | orjson.OPT_SERIALIZE_NUMPY
    | orjson.OPT_SERIALIZE_DATACLASS
    | orjson.OPT_OMIT_MICROSECONDS
)


class VerificationMethod(StrEnum):
    EMAIL = auto()
    INN = auto()
    SOCIAL = auto()


API_URL = "/api/v1"
