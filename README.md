# yawm

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/devalv/yawm/branch/main/graph/badge.svg)](https://codecov.io/gh/devalv/yawm)

For any additional instructions please see [Wiki](https://github.com/devalv/yawm/wiki).

## Project directory structure

### backend

```bash
├── core
│   ├── database
│   │   ├── models
│   │   └── migrations
│   ├── schemas
│   ├── services
│   ├── utils
│   ├── .env
│   └── config.py
├── tests
│   ├── snapshots
│   └── conftest.py
├── api
│   └── v1
│       └── handlers
├── main.py
└── .coveragerc
```

#### root

Project outer-startup files, such as:

* alembic configuration
* pytest configuration
* uvicorn app file
* project requirements lists
* coverage configuration

#### core

Core project features such as:

* settings (config.py)
* database migrations and models
* services (business logic)
* schemas (pydantic models)
* utils (extra utils, such as fastapi-pagination custom Page)

#### tests

Project tests

#### api

Project API by versions (v1, v2 and etc.).

### docker

Docker-images and docker-compose configuration files.

#### docker registry

```bash
docker login
docker build . -f backend/docker/python/Dockerfile -t devalv/yawm:backend
docker push devalv/yawm:backend
```

#### mypy

```bash
mypy --config-file=tox.ini core api
```
