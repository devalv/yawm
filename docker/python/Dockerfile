FROM python:3.8-slim
WORKDIR /opt/yawm/app
RUN pip install pipenv
ADD backend/Pipfile .
ADD backend/Pipfile.lock .
RUN pipenv install --dev
