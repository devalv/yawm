[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/devalv/yawm/branch/main/graph/badge.svg?token=61KST8QUNE)](https://codecov.io/gh/devalv/yawm)

# yawm
For additional instructions please see
[Wiki](https://github.com/devalv/yawm/wiki)

**API schema** based on [**JSON API**](https://jsonapi.org)

## Project directory structure

### backend
```
├── core
│   ├── database
│   │   ├── models
│   │   └── migrations
│   ├── schemas
│   ├── services
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
#### root-dir
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

#### tests
Project tests

#### api
Project API by versions (v1, v2 and etc.).


### docker
Docker-images and docker-compose configuration files.
