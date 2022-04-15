from functools import lru_cache
from typing import Any, Dict, Optional, Set, Union

from jose.constants import ALGORITHMS
from pydantic import BaseSettings, PostgresDsn, validator
from starlette.datastructures import Secret

BoolOrStr = Union[bool, str]


class ProjectPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres", "postgresql"}


class Settings(BaseSettings):

    # DB configuration
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: Union[Secret, str]
    DB_NAME: str
    DB_POOL_MIN_SIZE: int = 1
    DB_POOL_MAX_SIZE: int = 16
    DB_ECHO: BoolOrStr = False
    DB_SSL: Optional[bool] = None
    DB_USE_CONNECTION_FOR_REQUEST: BoolOrStr = True
    DB_RETRY_LIMIT: int = 1
    DB_RETRY_INTERVAL: int = 1
    DATABASE_URI: Optional[ProjectPostgresDsn] = None

    # security
    SECRET_KEY: Union[Secret, str]
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
    API_PROTOCOL: str = "https"  # TODO: ?
    API_LOCATION: str = f"{API_PROTOCOL}://{API_DOMAIN}:{API_PORT}"  # TODO: ?

    # third-party services
    SENTRY_DSN: Optional[Union[Secret, str]] = None
    SENTRY_ENVIRONMENT: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, value: Optional[str], values: Dict[str, Any]
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
    def wrap_secret(cls, value: Union[Secret, str]) -> Secret:
        if isinstance(value, Secret) or value is None:
            return value
        return Secret(value)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings():
    """Cached app settings.

    Example: settings: config.Settings = Depends(get_settings)
    """
    return Settings()
