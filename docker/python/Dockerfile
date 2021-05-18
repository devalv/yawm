FROM python:3.9-slim
WORKDIR /opt/yawm/app
RUN apt-get update && apt-get install -y gcc python3-dev python3-setuptools
ADD backend/Pipfile* ./
RUN pip install pipenv
RUN pipenv install --dev
