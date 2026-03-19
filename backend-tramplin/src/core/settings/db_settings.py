from pydantic import BaseModel
from pydantic import SecretStr


class DatabaseSettings(BaseModel):

    user: str
    password: SecretStr
    host: str
    port: int

    connection_url: str = ...
