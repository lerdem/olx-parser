FROM python:3.9-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD app.py /app
RUN pip3 install -r requirements.txt
COPY . /app
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "app:app"]
