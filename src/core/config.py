from zoneinfo import ZoneInfo

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.const import (DEFAULT_TIMEZONE, ENV_FILE_ENCODING, ENV_FILE_NAME,
                        ENV_NESTED_DELIMETER)


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding=ENV_FILE_ENCODING,
        env_nested_delimiter=ENV_NESTED_DELIMETER,
    )

    # default_timezone: ZoneInfo = ZoneInfo(DEFAULT_TIMEZONE)
    default_file_type: str = "application/octet-stream"

    default_host: str = "localhost"
    default_port: int = 8000
    server_reload: bool = True

    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int
    postgres_driver: str
    postgres_db: str

    @property
    def db_conn_link(self) -> str:
        return f"{self.postgres_driver}://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Config()
