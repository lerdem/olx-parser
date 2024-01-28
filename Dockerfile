FROM python:3.9-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -U pip
RUN pip install -r requirements.txt
#ADD requirements-test.txt /app
#RUN pip install -r requirements-test.txt
COPY . /app
