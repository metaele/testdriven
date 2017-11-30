FROM python:3.6.3-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/

RUN apk add --update --no-cache \
    postgresql-client \
    postgresql-dev \
    libpq \
    gcc \
    python3-dev \
    musl-dev && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del -r python3-dev postgresql-client postgresql-dev gcc musl-dev

ADD . /usr/src/app/

CMD flask run -h 0.0.0.0
