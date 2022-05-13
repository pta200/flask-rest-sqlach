# syntax=docker/dockerfile:1

FROM python:3.6

WORKDIR /app

COPY . .

#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "./guinicorn.sh"]
