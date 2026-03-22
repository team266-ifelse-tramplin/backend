from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.db_settings import DatabaseSettings
from zoneinfo import ZoneInfo
from const import ENV_FILE_NAME, ENV_FILE_ENCODING, ENV_NESTED_DELIMETER, DEFAULT_TIMEZONE


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding=ENV_FILE_ENCODING,
        env_nested_delimiter=ENV_NESTED_DELIMETER,
    )

    db: DatabaseSettings

    default_timezone: ZoneInfo = ZoneInfo(DEFAULT_TIMEZONE)
    default_file_type: str = "application/octet-stream"


settings = Config()




