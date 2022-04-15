from functools import lru_cache
from typing import Any, Dict, Set

from jose.constants import ALGORITHMS
from pydantic import BaseSettings, PostgresDsn, validator
from starlette.datastructures import Secret

BoolOrStr = bool | str
BoolOrNone = bool | None


class ProjectPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres", "postgresql"}


class Settings(BaseSettings):

    # DB configuration
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: Secret | str
    DB_NAME: str
    DB_POOL_MIN_SIZE: int = 1
    DB_POOL_MAX_SIZE: int = 16
    DB_ECHO: bool | str = False
    DB_SSL: BoolOrNone = None
    DB_USE_CONNECTION_FOR_REQUEST: BoolOrStr = True
    DB_RETRY_LIMIT: int = 1
    DB_RETRY_INTERVAL: int = 1
    DATABASE_URI: ProjectPostgresDsn | None = None

    # security
    SECRET_KEY: Secret | str
    ALGORITHM: str = ALGORITHMS.HS256
    ALLOW_ORIGINS: Set[str] = set()
    ACCESS_TOKEN_EXPIRE_MIN: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SWAG_LOGIN_ENDPOINT: str = "/api/v1/swag_login"
    SWAG_SWAP_TOKEN_ENDPOINT: str = "/api/v1/swag_swap_token"
    REACT_SWAP_TOKEN_ENDPOINT: str = "/api/v1/react_swap_token"

    # client application endpoints
    FRONTEND_DOMAIN: str = "localhost"
    FRONTEND_PORT: int = 3000
    FRONTEND_PROTOCOL: str = "https"
    FRONTEND_URL: str = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}:{FRONTEND_PORT}"
    FRONTEND_AUTH_TOKEN_PARAM: str = "authToken"
    FRONTEND_AUTH_URL: str = f"{FRONTEND_URL}?{FRONTEND_AUTH_TOKEN_PARAM}"

    # API configuration
    CRAWLER_USER_AGENT: str = "yawm-api"
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_DOMAIN: str = "localhost"

    # third-party services
    SENTRY_DSN: Secret | str | None = None
    SENTRY_ENVIRONMENT: str | None = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, value: str, values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(value, str):
            return value

        return ProjectPostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=str(values.get("DB_PASSWORD")),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f'/{values.get("DB_NAME") or ""}',
        )

    @validator("SECRET_KEY", "DB_PASSWORD", "SENTRY_DSN", pre=True)
    def wrap_secret(cls, value: Secret | str) -> Secret:
        if isinstance(value, Secret) or value is None:
            return value
        return Secret(value)

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        case_sensitive: bool = True


@lru_cache()
def get_settings() -> Settings:
    """Cached app settings.

    Example: settings: config.Settings = Depends(get_settings)
    """
    return Settings()
