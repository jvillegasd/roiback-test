  
FROM python:3.7 

LABEL Author="Johnny Villegas"
LABEL version="1.0"

RUN mkdir -p /mysite
WORKDIR /mysite

# Install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .

# Install requirements
RUN pip3 install -r requirements.txt
RUN python 