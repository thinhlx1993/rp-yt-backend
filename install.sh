#!bin/bash
cd /opt
apt update && apt install build-essential python3 python3-pip python3-dev -y
pip3 install --upgrade setuptools
apt install git -y && git clone https://github.com/thinhlx1993/rp-yt-backend.git
cd rp-yt-backend && pip3 install -r requirements.txt
pip3 install -U selenium -y
chmod +x -R /opt/rp-yt-backend/etc
mkdir /opt/rp-yt-backend/logs
apt install firefox -y
apt upgrade firefox -y
cp /opt/rp-yt-backend/celery@worker.service /etc/systemd/system/
systemctl daemon-reload
systemctl start celery@worker
systemctl enable celery@worker
