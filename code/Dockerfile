FROM python:3.11

RUN pip install poetry

ARG MONOREPO_APP_PATH

RUN test -n "${MONOREPO_APP_PATH}"

WORKDIR /usr/src/monorepo

COPY shared /usr/src/monorepo/shared
COPY ${MONOREPO_APP_PATH} /usr/src/monorepo/${MONOREPO_APP_PATH}

WORKDIR /usr/src/monorepo/${MONOREPO_APP_PATH}

RUN poetry install --compile

ENTRYPOINT ["./run.sh"]
