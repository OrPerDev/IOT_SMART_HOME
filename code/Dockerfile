FROM python:3.11

ARG MONOREPO_APP_PATH

RUN test -n "${MONOREPO_APP_PATH}"

WORKDIR /usr/src/monorepo

RUN pip install poetry

COPY shared /usr/src/monorepo/shared
COPY ${MONOREPO_APP_PATH} /usr/src/monorepo/${MONOREPO_APP_PATH}

WORKDIR /usr/src/monorepo/${MONOREPO_APP_PATH}

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "ac.py"]
