from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    API_HOST: str
    API_PORT: int

    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str
    ADMIN_NAME: str
    ADMIN_SURNAME: str
    ADMIN_PATRONYMIC: str

    COMMON_EMAIL: EmailStr
    COMMON_PASSWORD: str
    COMMON_NAME: str
    COMMON_SURNAME: str
    COMMON_PATRONYMIC: str

    TRANSACTION_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
