FROM python:3.10.8-alpine as development_build

ARG APP_DIR=/src

ARG ENV

ENV ENV=${ENV} \
    PYTHOPNUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3

COPY /src /src/
COPY pyproject.toml /pyproject.toml
COPY poetry.lock /poetry.lock
COPY README.md /README.md


# System dependencies
RUN pip install "poetry==$POETRY_VERSION"

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --only main

WORKDIR $APP_DIR

CMD ["poetry", "run", "hello"]