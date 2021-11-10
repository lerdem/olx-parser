FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
RUN apt update && apt install -y gcc && python -m pip install --upgrade pip

ADD requirements.txt /app
RUN pip install -r requirements.txt
RUN apt remove -y gcc && apt autoremove -y
COPY . /app
CMD ["uwsgi", "wsgi.ini"]
