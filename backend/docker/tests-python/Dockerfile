FROM devalv/yawm-backend:latest

USER root

COPY ./backend/ .
# chown all the files to the app user
RUN chown -R app:app $APP_HOME

RUN poetry export --dev -f requirements.txt --output dev-requirements.txt
RUN pip install -r dev-requirements.txt

# change to the app user
USER app

# run tests
CMD python -m pytest
