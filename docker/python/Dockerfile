FROM python:3.9-slim
WORKDIR /opt/yawm/app
RUN apt-get update && apt-get install -y gcc python3-dev python3-setuptools
RUN pip install --upgrade pip
ADD backend/*requirements.txt ./
RUN pip install --use-deprecated=legacy-resolver -r requirements.txt && pip install --use-deprecated=legacy-resolver -r dev-requirements.txt
