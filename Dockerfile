FROM ubuntu:16.04

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y git wget build-essential python3 python3-dev python3-pip firefox

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:5000 --timeout 60 --workers 2 --threads 4 --access-logfile - "app.app:create_app()"
