  
FROM python:3.7 

LABEL Author="Johnny Villegas"
LABEL version="1.0"

RUN mkdir -p /mysite
WORKDIR /mysite

COPY requirements.txt .

# Install requirements
RUN pip3 install -r requirements.txt
RUN python 