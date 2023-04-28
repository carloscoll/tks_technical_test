FROM python:3.9-alpine

ARG POETRY_HOME=/opt/poetry

WORKDIR /opt/app

ENV PATH="${PATH}:${POETRY_HOME}/bin"                                                               \
    PYTHONUNBUFFERED=1                                                                              \
    POETRY_VIRTUALENVS_CREATE=false                                                                 \
    APP_DIR=/opt/app

WORKDIR ${APP_DIR}

COPY poetry.lock                    ${APP_DIR}/poetry.lock
COPY pyproject.toml                 ${APP_DIR}/pyproject.toml
COPY main.py                        ${APP_DIR}/main.py

RUN apk add --update --no-cache                                                                     \
    curl                                                                                            \
    build-base                                                                                      \
    libffi-dev                                                                                      \
    postgresql-dev

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 -           && \
    poetry config virtualenvs.create false                                                       && \
    poetry install --no-interaction

EXPOSE 5050
EXPOSE 5432

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]