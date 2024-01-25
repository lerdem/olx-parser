FROM python:3.9-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . /app
