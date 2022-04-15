# Yet another wishlist maker - YAWM

[![FastAPI](https://shields.io/static/v1?label=FastAPI&message=0.75&color=green)](https://github.com/tiangolo/fastapi)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/devalv/yawm/branch/main/graph/badge.svg?token=61KST8QUNE)](https://codecov.io/gh/devalv/yawm)
[![CodeQL](https://github.com/devalv/yawm/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/devalv/yawm/actions/workflows/codeql-analysis.yml)

For any additional instructions please see [Wiki](https://github.com/devalv/yawm/wiki).

## Git branches

```bash
main - production branch
fix/bug-name - production bug fixes
release/fastapi-*.*.* - ongoing release
feature/feature-name - feature branch for ongoing release
```

## Project directory structure

### backend

```bash
├── docker
├── core
│   ├── database
│   │   ├── models
│   │   └── migrations
│   ├── schemas
│   │   └── security
│   ├── services
│   ├── health
│   ├── utils
│   └── config.py
├── tests
│   ├── snapshots
│   ├── .env
│   └── conftest.py
├── api
│   ├── v1
│   │   ├── handlers
│   │   └── schemas
│   └── v2
│       ├── handlers
│       └── schemas
├── main.py
├── .env
├── alembic.ini
└── pyproject.toml
```

#### root

Project outer-startup files, such as:

* alembic configuration
* pytest, coverage, flake8, etc configurations (pyproject.toml)
* uvicorn app file
* project requirements lists

#### core

Core project features such as:

* settings (config.py)
* database migrations and models
* services (business logic)
* schemas (pydantic models)
* utils (extra utils, such as fastapi-pagination custom Page)
* health (health check endpoint)

#### tests

Project tests

#### api

Project API by versions (v1, v2 and etc.).
