Create Environment
----------
    - Install redis, mongodb
    - cd /opt && git clone https://bitbucket.org/BootAI/crypto-backend.git
    - cd crypto-backend/app looking for file setting.py and extension.py edit address to your server address
    - CELERY_BROKER_URL = 'redis://:1234567a@@@<your-server-address>:6379/0'
    - CELERY_BACKEND_URL = 'redis://:1234567a@@@<your-server-address>:6379/0'
    - REDIS_URL = "redis://:1234567a@@@<your-server-address>:6379/0"
    - sudo apt-get update
    - sudo apt-get install python3-dev python3-pip
    - sudo apt-get install build-essential
    - pip install -r requirements.txt

Install Docker (Production mode)
----------
    
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    $ sudo apt-get update
    
    $ apt-cache policy docker-ce

    $ sudo apt-get install -y docker-ce

    $ sudo systemctl status docker

Install Docker-Compose (Production mode)
----------

    $ sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.15.0/docker-compose-$(uname -s)-$(uname -m)"

    $ sudo chmod +x /usr/local/bin/docker-compose

    $ docker-compose -v


Build Backend (Production mode)
----------

    $ cd /opt/voice-newsfeed-backend/

    $ sudo /usr/local/bin/docker-compose up --build -d

    # need several minutes to build docker image

Auto rebuild when restart server (Production mode)
----------

    # copy all content in /opt/voice-newsfeed-backend and paste to /etc/systemd/system/newsfeed.service

    $ sudo nano /etc/systemd/system/newsfeed.service

    $ sudo systemctl start newsfeed

    $ sudo systemctl enable newsfeed


Generating models (if you are using mysql and want to rebuild model)
----------

    $ pip install flask-sqlacodegen

    $ flask-sqlacodegen --flask --outfile models.py mysql://username:password@host/db


Starting server dev
----------
    $ python manage.py # run main server
    $ celery -A app.celery.celery worker --loglevel=info run celery server using for send email register, verify vv.v..
    $ celery beat -A app.celery --schedule=tmp/celerybeat-schedule --loglevel=INFO --pidfile=tmp/celerybeat.pid
    $ celery worker -A app.celery --pool=solo --loglevel=INFO
    $ pyinstaller --add-data "app/template;app/template" --add-data "etc;etc" --add-data "logs;logs" --hidden-import "PyQt5.sip" --hidden-import "celery.fixups" --hidden-import "celery.fixups.django" --hidden-import "pandas._l
ibs.tslibs.np_datetime" --hidden-import "pandas._libs.tslibs.nattype" --hidden-import "pandas._libs.skiplist" manage.py -y
