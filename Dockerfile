FROM python:3.9-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT ["/bin/sh"]
CMD ["./entrypoint.sh"]
