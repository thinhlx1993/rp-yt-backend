#!bin/bash
cd /opt
apt update && apt install build-essential python3 python3-pip python3-dev -y
apt install git -y && git clone https://github.com/thinhlx1993/rp-yt-backend.git && git checkout develop
cd rp-yt-backend && pip3 install -r requirements.txt
chmod +x -R /opt/rp-yt-backend/etc
mkdir /opt/rp-yt-backend/logs
apt install firefox -y
# apt upgrade firefox -y
apt-get install openvpn -y
apt install golang-go -y
cd /opt && git clone https://github.com/adtac/autovpn
cd autovpn
go build autovpn.go
install autovpn /usr/local/bin/
apt-get install macchanger -y
cp /opt/rp-yt-backend/etc/config/report@worker.service /etc/systemd/system/
cp /opt/rp-yt-backend/etc/config/fakeip@worker.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable report@worker
systemctl enable fakeip@worker
reboot