#!bin/bash
cd /opt
apt update && apt install build-essential python3 python3-pip python3-dev -y
apt install git -y && git clone https://github.com/thinhlx1993/rp-yt-backend.git && git checkout develop
cd rp-yt-backend && pip3 install -r requirements.txt
pip3 install -U selenium -y
chmod +x -R /opt/rp-yt-backend/etc
mkdir /opt/rp-yt-backend/logs
apt install firefox -y
apt upgrade firefox -y
apt-get install openvpn -y
cp /opt/rp-yt-backend/etc/config/report@worker.service /etc/systemd/system/
cp /opt/rp-yt-backend/etc/config/fakeip@worker.service /etc/systemd/system/
systemctl daemon-reload
systemctl start report@worker
systemctl enable report@worker
systemctl start fakeip@worker
systemctl enable fakeip@worker