# Builder Stage
FROM docker.io/python:3.12-slim AS build-backend

ENV PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ADD https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip /EasyOCR/
ADD https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip /EasyOCR/

RUN apt-get update && \
    apt-get install unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /EasyOCR
RUN unzip /EasyOCR/craft_mlt_25k.zip && unzip /EasyOCR/english_g2.zip

RUN pip install -U pip setuptools wheel -q && \
    pip install poetry==1.8.3 -q

WORKDIR /srv

COPY ./pyproject.toml ./poetry.lock /srv/
RUN poetry install --only main --no-root --sync --no-cache
COPY src/ /srv/src

# Runtime Stage
FROM unit:python3.12-slim

ENV EASYOCR_MODULE_PATH=/EasyOCR

COPY --from=build-backend /srv /srv
COPY --from=build-backend /EasyOCR/craft_mlt_25k.pth /EasyOCR/model/
COPY --from=build-backend /EasyOCR/english_g2.pth /EasyOCR/model/
RUN mkdir /EasyOCR/user_network

WORKDIR /srv

COPY ./unit.config.json /docker-entrypoint.d/config.json
