FROM python:3.5.4-slim

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y git && apt-get install -y build-essential && \
    apt-get install -y libevent-dev python-all-dev && \
    apt-get install -y libmysqlclient-dev && \
    apt-get install firefox -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:5000 --timeout 60 --workers 2 --threads 4 --access-logfile - "app.app:create_app()"
