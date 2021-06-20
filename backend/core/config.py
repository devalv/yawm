# -*- coding: utf-8 -*-
"""Project configuration file (Starlette)."""

from sqlalchemy.engine.url import URL, make_url

from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")
# Gino
DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config("DB_PORT", cast=int, default=None)
DB_USER = config("DB_USER", cast=str, default=None)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_DATABASE", default=None)
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=1)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)
# uvicorn
API_HOST = config("API_HOST", default="127.0.0.1")
API_PORT = config("API_PORT", cast=int, default=8000)
# crawler User-Agent
CRAWLER_USER_AGENT = config("CRAWLER_USER_AGENT", default="yawm-api")
# security
API_DOMAIN = config("API_DOMAIN", default=None)
SECRET_KEY = config("SECRET_KEY", default=None)
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MIN = config("ACCESS_TOKEN_EXPIRE_MIN", default=30)
# Google OAuth2 configuration
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default=None)
GOOGLE_CLIENT_SECRETS_JSON = config("GOOGLE_CLIENT_SECRETS_JSON", default=None)
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/userinfo.profile"]
# TODO: cert keys should be replaced from time to time and stored on cache
# https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CERT_KEYS = {
  "6a1d26d992be7a4b689bdce1911f4e9adc75d9f1": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIDaloSJx4JogwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0yMTA2MDQwNDI5NTVaFw0yMTA2MjAxNjQ0NTVaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDLgP1t76jwwpllimv0aCao0XD+kfRruM8N\nYbXNgzAVRVIMJjfRawEAMZGQNYopZOBVD2/Nl2M+HVax98EwPvWCGfTpSHHyUJvF\n6Yzrg31UYGaUs3bpp677MkBVuVsSOdOHfmv4tcPpMp1By+bcIO9HehNniPXHkb5i\nKXkkp6+9snxa73xUiqBOPH5FB/4SpNq71u3HMITPHDkvEP8N720rePza+jsVdYdn\nleahjpO9B8kdkPShPq1CCq2AI3Vr8L3FXeg6dJK0Fb1Xflu5Bfdwxh/WVrszenOy\nTseuVA/phOdAS2zxTwt7DNwFTACCRNxWKBTHqhY0t9oElnhvCAEFAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQCuQxUtRYlB61Jj6Z9bVpjDhcsmuava\nmg5pGek1f5OZdlpYh68Sh0bSIIFhnmcuy0al48vlmdWG9t8HGltlXZczR5Rkizmd\nTJLaOeXdRtprN8j+oAf/h16+6Y8tmctWNdh/V90JpaChujmTBz3aoTC/xAEfj8Ln\n2TTTt5+IgfRgqcJZjZ026Seo3o5oHzstoIPYSbvv4pIBvuDg8VLP0vriltGvU61k\nxSCHZFYskasFOmuJUvJdkxrNpdvmZc84a1OyH78CTp24n777J3h5Kb4+N8cueMC7\nvRvZvyMXhD78gWCsTFF76zwtstVTrCUGJ33vx8Ykt5QomqkyTicoORw5\n-----END CERTIFICATE-----\n",
  "19fe2a7b6795239606ca0a750794a7bd9fd95961": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIVGBFY93ZYokwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0yMTA2MTIwNDI5NTVaFw0yMTA2MjgxNjQ0NTVaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDRi52e+K7A11wKhcQzAyUlaHFZimYB5FdD\nwN/lsJV/nEVUSYvlqb/ZNNZHBF/fi+om6ganJ/dLvMl4m/wjYvK+anDfctF5ESQ5\nsK3W6nXskbDn930rYx/n0Sec+R3thQaSVTGN7yvEguJOGI90RoXw/mlF575YPaaZ\nBK6DSuo2Uylp1hVoy/dj8cuv3sd6HUAJGh9h+/aGYZKYLqijRI3h3mA/7+CADOD0\nqjssNVwGDpNYB8kuHfcaky0AjYw+N3pcUmO75H13rwgMIhSj4ITwrSkBmdcZLxpa\nWf92mNmGUyNeuBjjbdBrhg2yWg9zCRDbSuTxcZgWvQf/0a5YhpZZAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQCrfG7K0x6L/Y9Sj/Au3GraEX3lPScu\n5AuW7tP26iYMf69n4m8Vi/UtkiHbZJeOWQ0HNgevq50ke8MHXOMBoHMfcjEsPyxu\nfWRtIsqNWnNCWgbfSTIhk/NLHbZKnSbW+qysLcDNMrFc1XEaMR7i0XTQE8tNPfV9\nNJSI+scn6Oq/z6Tjdw+iSbqkw8n8+PfSRl0J8hx6gEQoKFagw1Zt/jAApSW6SWKb\ny4VwFHgTVDbPwdMV4VbseKKx66Lb8qGPqTu8TM70nQlIHUnbXccalXGOaQsycaaN\nWPGpychl1JxUftwbdaW/dY5NVpGEwXJ2DRAJiNK6jDcSsrjOJI4d7ukb\n-----END CERTIFICATE-----\n",
  "112e4b52ab833017d385ce0d0b4c60587ed25842": "-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIRAoQks63w4EwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0yMTA2MjAwNDI5NTdaFw0yMTA3MDYxNjQ0NTdaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCsf17gul45G1GRC6jm8ov5yws+cmbJZT+o\neI6pbJdWyg/KZQoiY2w+Vps5y+RhiU9+VYT6qa1AIf4AIOPHMKHIiS2v7nN4IRmJ\n2WfylYSYOr5H5peL+xCAlSv7sf9jr2EPxxHQrcvILzpBFumKDFbwXqFRT1qP/1Va\n5XCwy8uJCdtvNLgJa+L9bMhb2IbSA62GyyV99r/quqhCkdzQZ+wS7d73vVBlwnIz\nGvqm1j9u9PAhirBG/2m3G0pMyqi9XpgE3mf8uEIOaTWAEuZJ6PqZ8dJbaKjpNdlp\nXc9rIvZRO17qqu8CQX9FdS1V64PGbixxR7VF1/5N2wBcWbUo82rjAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQCGOTPITDKeIsTJhueXYtp9t3u0L8Id\nO58xb5dDbNGbi9E/C0cdDq8SfdFBHvOL8eJJSjzCRefRi1NhMlWaWsT471GgXdUV\nHR0CSV87Gj6BvMcAq9WFQu9k6LFtN2qp8CsFFEbjgPW3GFSXriy0W/VRzmb4aUbz\nVjo+EOTAiQP05qQ0bahaXWxXyftctMqpmM/EjFKZZwSH2fuFRNiq+0prIG8xRUYp\nakyr4D+GC0RrUpCa2SfGoojSYQPlQfkZGyeGLBi1UQImCKBJ8wYVaSIaVlLHYZik\nu/lQUGTPW3NLCn0id4AKAx3Ojf0t2jhsPy9u7kW5mPQA/CeRWjsPZ2uX\n-----END CERTIFICATE-----\n"
}
# new
LOGIN_ENDPOINT = "/api/v1/login"
SWAP_TOKEN_ENDPOINT = "/api/v1/swap_token"

