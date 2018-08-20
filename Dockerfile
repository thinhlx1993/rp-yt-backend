FROM python:3.5.4-slim

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y git && apt-get install -y build-essential && apt-get install -y wget && \
    apt-get install -y libevent-dev python-all-dev && \
    apt-get install -y libmysqlclient-dev && \
    add-apt-repository ppa:mozillateam/ppa && \
    cd /usr/local && wget http://ftp.mozilla.org/pub/firefox/releases/61.0/linux-x86_64/en-US/firefox-61.0.tar.bz2 && \
    tar xvjf firefox-61.0.tar.bz2 && \
    ln -s /usr/local/firefox/firefox /usr/bin/firefox

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:5000 --timeout 60 --workers 2 --threads 4 --access-logfile - "app.app:create_app()"
