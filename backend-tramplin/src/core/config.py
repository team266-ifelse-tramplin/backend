from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.db_settings import DatabaseSettings
from const import ENV_FILE_NAME, ENV_FILE_ENCODING, ENV_NESTED_DELIMETER


class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding=ENV_FILE_ENCODING,
        env_nested_delimiter=ENV_NESTED_DELIMETER,
    )

    db: DatabaseSettings



