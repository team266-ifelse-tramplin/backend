from zoneinfo import ZoneInfo

from const import (DEFAULT_TIMEZONE, ENV_FILE_ENCODING, ENV_FILE_NAME,
                   ENV_NESTED_DELIMETER)
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.db_settings import DatabaseSettings


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding=ENV_FILE_ENCODING,
        env_nested_delimiter=ENV_NESTED_DELIMETER,
    )

    db: DatabaseSettings

    default_timezone: ZoneInfo = ZoneInfo(DEFAULT_TIMEZONE)
    default_file_type: str = "application/octet-stream"

    default_host: str = "localhost"
    default_port: str = "8000"
    server_reload: bool = True


settings = Config()
