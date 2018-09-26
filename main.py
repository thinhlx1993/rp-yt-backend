import sys
import time
import _thread
import random
import subprocess
import webbrowser
from PyQt5 import QtWidgets, QtCore, QtGui
from app.app import create_app
from app.settings import DevConfig, ProdConfig, os
from app.browser.report_video import start_app
from pymongo import MongoClient


def FlaskThread():
    config = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig
    application = create_app(config_object=config, name='server')
    application.run(port=5000, use_reloader=False, debug = False)


def run_command(command):
    p = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE)
    p.communicate()
    return p.returncode
    # print(p.returncode) # is 0 if success

def report_user_func():
    # report user
    while True:
        client = MongoClient()
        db = client['test-yt']
        totals_mac = db.mac_address.count_documents({})
        mac = db.mac_address.find({}).limit(-1).skip(random.randint(0, totals_mac)).next()
        mac_address = mac['mac'].replace(':', '')
        fh = open("E:\\Code\\rp-yt-backend\\etc\\fakeip\\fake_mac.bat","w")
        fh.write("netsh interface set interface \"Mobile\" disable \n")
        fh.write("reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0001 /v NetworkAddress /d ")
        fh.write(mac_address)
        fh.write(" /f \n")
        fh.write("netsh interface set interface \"Mobile\" enable")
        fh.close()
        client.close()
        run_command("E:\\Code\\rp-yt-backend\\etc\\fakeip\\fake_mac.bat")
        open("E:\\Code\\rp-yt-backend\\etc\\fakeip\\fake_mac.bat","w").close()
        print('Connecting')
        run_command("E:\\Code\\rp-yt-backend\\etc\\fakeip\\start.bat")
        time.sleep(10)
        start_app()
        print('Stopping')
        run_command("E:\\Code\\rp-yt-backend\\etc\\fakeip\\stop.bat")
        time.sleep(10)


def report_video_func():
    while True:
        client = MongoClient()
        db = client['test-yt']
        # totals_mac = db.mac_address.count_documents({})
        # mac = db.mac_address.find({}).limit(-1).skip(random.randint(0, totals_mac)).next()
        # mac_address = mac['mac'].replace(':', '')
        # fh = open("E:\\Code\\rp-yt-backend\\etc\\fakeip\\fake_mac.bat","w")
        # fh.write("netsh interface set interface \"Ethernet 2\" disable \n")
        # fh.write("reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\\0014 /v NetworkAddress /d ")
        # fh.write(mac_address)
        # fh.write(" /f \n")
        # fh.write("netsh interface set interface \"Ethernet 2\" enable")
        # fh.close()
        # client.close()
        # print('Connecting')
        # run_command("E:\\Code\\rp-yt-backend\\etc\\fakeip\\fake_mac.bat")
        # open("E:\\Code\\rp-yt-backend\\etc\\fakeip\\fake_mac.bat","w").close()
        # run_command("E:\\Code\\rp-yt-backend\\etc\\fakeip\\change_ip_hma.bat")
        # time.sleep(10)
        start_app()


def ReportingThread():
    # report_user_func()
    # Report video
    report_video_func()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        menu.addAction("Exit")
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)

        # Reporting youtube
        _thread.start_new_thread(ReportingThread,())
        
        # start flask server
        _thread.start_new_thread(FlaskThread,())
        webbrowser.open_new_tab('http://localhost:5000')
        webbrowser.open_new_tab('https://whoer.net')


    def exit(self):
        QtCore.QCoreApplication.exit()


def main(image):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    ion='icon.png'
    main(ion)