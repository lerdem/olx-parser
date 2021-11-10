FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && python -m pip install --upgrade pip

ADD requirements.txt /app
RUN pip install -r requirements.txt
RUN apt-get remove -y gcc && apt-get autoremove -y
COPY . /app
CMD ["uwsgi", "wsgi.ini"]
