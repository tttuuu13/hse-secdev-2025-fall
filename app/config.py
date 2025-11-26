from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: SecretStr = "sqlite:///./test.db"
    secret_key: SecretStr = "insecure-default-key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
