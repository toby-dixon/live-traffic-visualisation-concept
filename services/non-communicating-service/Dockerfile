FROM python:3.11-alpine3.22 AS build

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-alpine3.22 AS run

WORKDIR /app

COPY --from=build /install /usr/local
