FROM python:3.7.4-alpine

EXPOSE 5000

WORKDIR /app

COPY ./app/requirements.txt /app

RUN apk add python3-dev
RUN apk add libevent-dev
RUN apk add mysql-client
RUN apk add mariadb-dev

RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt

ENV FLASK_APP=app/main.py

ENV FLASK_ENV=Development

ENV FLASK_DEBUG=True

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

COPY . .

CMD flask run -h 0.0.0.0