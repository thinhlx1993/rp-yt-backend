import sys
import time
import _thread
import random
import subprocess
import webbrowser
import socket
from PyQt5 import QtWidgets, QtCore, QtGui
from app.app import create_app
from app.model import Video
from app.settings import DevConfig, ProdConfig, os
from app.browser.report_video import start_app
from sqlalchemy import create_engine
engine = create_engine('sqlite:///etc/db/prd.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy.sql.expression import func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Text
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Mac(Base):
    __tablename__ = 'mac'
    id = Column(Integer, primary_key=True)
    mac = Column(Text)
    created_date = Column(Integer)

    @classmethod
    def find_random(cls):
        rand = random.randrange(0, session.query(Mac).count())
        row = session.query(Mac)[rand]
        return row

    @classmethod
    def find_by_id(cls, agent_id):
        return cls.query.filter_by(id=agent_id, status=True).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, status=True).first()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


def FlaskThread():
    config = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig
    application = create_app(config_object=config, name='server')
    application.run(port=5000, use_reloader=False, debug=False)


def run_command(command):
    p = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE)
    p.communicate()
    return p.returncode
    # print(p.returncode) # is 0 if success


def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname('www.google.com')
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False


def fake_ip_by_dcom():
    # report user
    while True:
        mac = Mac.find_random()
        mac_address = mac.mac.replace(':', '')
        fh = open("etc\\fakeip\\fake_mac.bat","w")
        fh.write("netsh interface set interface \"Mobile\" disable \n")
        fh.write("reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0001 /v NetworkAddress /d ")
        fh.write(mac_address)
        fh.write(" /f \n")
        fh.write("netsh interface set interface \"Mobile\" enable")
        fh.close()
        run_command("etc\\fakeip\\fake_mac.bat")
        open("etc\\fakeip\\fake_mac.bat","w").close()
        print('Connecting')
        run_command("etc\\fakeip\\start.bat")
        time.sleep(10)
        start_app(session)
        print('Stopping')
        run_command("etc\\fakeip\\stop.bat")
        time.sleep(10)


def fake_ip_by_hma():
    while True:
        # mac = Mac.find_random()
        # mac_address = mac.mac.replace(':', '')
        # fh = open(r"etc\fakeip\fake_mac.bat", "w")
        # fh.write("netsh interface set interface \"Ethernet\" disable")
        # fh.write('\n')
        # fh.write("reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0003 /v NetworkAddress /d ")
        # fh.write(mac_address)
        # fh.write(" /f \n")
        # fh.write("netsh interface set interface \"Ethernet\" enable")
        # fh.close()
        # print('Connecting')
        # run_command("etc\\fakeip\\fake_mac.bat")
        # open("etc\\fakeip\\fake_mac.bat", "w").close()

        # time.sleep(30)
        run_command("etc\\fakeip\\change_ip_hma.bat")
        time.sleep(30)

        start_app(session)


def add_new_videos():
    with open("etc/videos.txt", "r") as file:
        for line in file.readlines():
            line = line.replace("\\n", "")
            new_video = Video(name="Video", url=line, status="active",
                              count_success=0, count_fail=0,
                              first_time=random.randint(0, 40),
                              second_time=random.randint(0, 60))
            new_video.save_to_db()


def fake_ip_by_vipsock72():
    # report user
    # run_command("etc\\fakeip\\run_socks.bat")
    # time.sleep(5)

    while True:
        run_command("etc\\fakeip\\new_ip.exe")
        time.sleep(2)
        start_app(session)
        run_command("etc\\fakeip\\clear_ip.exe")
        time.sleep(5)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        menu.addAction("Exit")
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)

        # Reporting youtube
        _thread.start_new_thread(fake_ip_by_vipsock72, ())
        
        # start flask server
        _thread.start_new_thread(FlaskThread,())
        # webbrowser.open_new_tab('http://localhost:5000')
        # webbrowser.open_new_tab('https://whoer.net')

    def exit(self):
        QtCore.QCoreApplication.exit()


def main(image):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    ion = 'icon.png'
    main(ion)
