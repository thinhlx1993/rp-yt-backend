import sys
import time
import _thread
import subprocess
import webbrowser
from PyQt5 import QtWidgets, QtCore, QtGui
from app.app import create_app
from app.settings import DevConfig, ProdConfig, os


def FlaskThread():
    config = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig
    application = create_app(config_object=config, name='server')
    application.run(port=5000, use_reloader=False, debug = False)


def ReportingThread():
    while True:
        print('Connecting')
        filepath="E:\\Code\\rp-yt-backend\\etc\\fakeip\\start.bat"
        p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

        p.communicate()
        # print(p.returncode) # is 0 if success
        time.sleep(10)
        print('Stopping')
        filepath="E:\\Code\\rp-yt-backend\\etc\\fakeip\\stop.bat"
        p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

        p.communicate()
        # print(p.returncode) # is 0 if success
        time.sleep(10)

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        menu.addAction("Exit")
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)

        # start flask server
        _thread.start_new_thread(FlaskThread,())
        webbrowser.open_new_tab('http://localhost:5000')

        # Reporting youtube
        _thread.start_new_thread(ReportingThread,())

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