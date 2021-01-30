FROM python:3.8-slim
WORKDIR /opt/yawm/app
RUN pip install pipenv
COPY backend/Pipfile backend/Pipfile.lock ./
RUN pipenv install --dev
