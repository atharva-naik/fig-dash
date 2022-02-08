import os
import sys
import pickle
# import logging
import functools
import threading

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
# logging.basicConfig(level=logging.DEBUG)
class Reply(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    def __init__(self, func, args=(), kwargs=None, parent=None):
        super().__init__(parent)
        self._results = None
        self._is_finished = False
        self._error_str = ""
        threading.Thread(
            target=self._execute, args=(func, args, kwargs), daemon=True
        ).start()

    @property
    def results(self):
        return self._results

    @property
    def error_str(self):
        return self._error_str

    def is_finished(self):
        return self._is_finished

    def has_error(self):
        return bool(self._error_str)

    def _execute(self, func, args, kwargs):
        if kwargs is None:
            kwargs = {}
        try:
            self._results = func(*args, **kwargs)
        except Exception as e:
            self._error_str = str(e)
        self._is_finished = True
        self.finished.emit()


def convert_to_reply(func):
    def wrapper(*args, **kwargs):
        reply = Reply(func, args, kwargs)
        return reply

    return wrapper


class Backend(QtCore.QObject):
    started = QtCore.pyqtSignal(QtCore.QUrl)
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = None

    @property
    def service(self):
        if self._service is None:
            reply = self._update_credentials()
            loop = QtCore.QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()
            if not reply.has_error():
                self._service = reply.results
            else:
                logging.debug(reply.error_str)
        return self._service

    @convert_to_reply
    def _update_credentials(self):
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                host = "localhost"
                port = 8080
                state = "default"
                QtCore.QTimer.singleShot(
                    0, functools.partial(self.get_url, flow, host, port, state)
                )
                creds = flow.run_local_server(
                    host=host, port=port, open_browser=False, state=state
                )
                self.finished.emit()
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build("oauth2", "v2", credentials=creds)

    def get_url(self, flow, host, port, state):
        flow.redirect_uri = "http://{}:{}/".format(host, port)
        redirect_uri, _ = flow.authorization_url(state=state)
        self.started.emit(QtCore.QUrl.fromUserInput(redirect_uri))

    @convert_to_reply
    def get_user_info(self):
        return self.service.userinfo().get().execute()


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.backend = Backend()

        self.webengineview = QtWebEngineWidgets.QWebEngineView()
        self.webengineview.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
        )
        self.webengineview.hide()
        button = QtWidgets.QPushButton("Sign in")

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button)
        lay.addWidget(self.webengineview)

        button.clicked.connect(self.sign_in)
        self.backend.started.connect(self.handle_url_changed)
        self.backend.finished.connect(self.webengineview.hide)

        self.resize(640, 480)

    def sign_in(self):
        reply = self.backend.get_user_info()
        wrapper = functools.partial(self.handle_finished_user_info, reply)
        reply.finished.connect(wrapper)

    def handle_finished_user_info(self, reply):
        if reply.has_error():
            logging.debug(reply.error_str)
        else:
            profile_info = reply.results
            print(profile_info)

    def handle_url_changed(self, url):
        self.webengineview.load(url)
        self.webengineview.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())