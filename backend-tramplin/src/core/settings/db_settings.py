from pydantic import BaseModel, SecretStr


class DatabaseSettings(BaseModel):

    user: str
    password: SecretStr
    host: str
    port: int
    driver: str
    db_name: str

    @property
    def db_conn_link(self) -> str:
        return f"{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db_name}"
