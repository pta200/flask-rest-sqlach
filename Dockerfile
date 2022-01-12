# syntax=docker/dockerfile:1

FROM python:3.6.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "./guinicorn.sh]
