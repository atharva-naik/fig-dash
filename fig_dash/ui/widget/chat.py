#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
# qt5 imports.
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.webview import DebugWebView


class ZoomFactor:
    '''browser zoom factor'''
    def __init__(self, zoom_factor):
        if zoom_factor > 5:
            zoom_factor /= 100
        zoom_factor = max(min(zoom_factor, 5), 0.25)
        self.value = zoom_factor

    def __str__(self):
        return f"zoom: {self.value}"

    def __repr__(self):
        return f"zoom: {self.value}"

    def __eq__(self, other):
        return self.value == other.value 

    def __lt__(self, other):
        return self.value < other.value 

    def __gt__(self, other):
        return self.value > other.value 

    def gt(self, zoom_factors):
        for value in zoom_factors:
            # print(f"{value.value} > {self.value}: {value > self}")
            if value > self: 
                return value
        return value

    def lt(self, zoom_factors):
        for value in zoom_factors:
            # print(value)
            if value.value < self.value: 
                return value
        return value

    def set(self, value):
        self.value = value

    def __call__(self):
        return self.value


class SilentWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, *args, **kwargs):
        '''silence javascript error mesages'''
        pass


class ChatWebView(DebugWebView):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(ChatWebView, self).__init__(parent)
        self.zoomFactors = [0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 5]
        self.zoomFactors = [ZoomFactor(zf) for zf in self.zoomFactors]
        self.loadFinished.connect(self.afterPageLoad)
        # silence js output log to the terminal (it is a hell hole of confusing).
        silent_page = SilentWebPage(self)
        self.setPage(silent_page)
        # link zooming related callbacks to shortcuts.
        self.CtrlPlus = QShortcut(QKeySequence.ZoomIn, self)
        self.CtrlPlus.activated.connect(self.zoomIn)
        self.CtrlMinus = QShortcut(QKeySequence.ZoomOut, self)
        self.CtrlMinus.activated.connect(self.zoomOut)
        self.CtrlK = QShortcut(QKeySequence("Ctrl+K"), self)
        self.CtrlK.activated.connect(self.changeUserAgent)

    def afterPageLoad(self):
        '''change the user agent every time on url reload.'''
        self.setZoomFactor(self.currentZoomFactor)
        self.changeUserAgent()

    def changeUserAgent(self):
        print("changing user agent.")
        try:
            self.page().profile().setHttpUserAgent(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
            )
            print("changed user agent.")
            # print("lol")
        except Exception as e:
            print(e) 

    def zoomIn(self):
        currentZoom = self.currentZoomFactor
        zoomFactor = ZoomFactor(currentZoom).gt(
            self.zoomFactors
        ).value
        self.setZoomFactor(zoomFactor)
        self.currentZoomFactor = zoomFactor

    def zoomOut(self):
        currentZoom = self.currentZoomFactor
        zoomFactor = ZoomFactor(currentZoom).lt(
            self.zoomFactors[::-1]
        ).value
        self.setZoomFactor(zoomFactor)
        self.currentZoomFactor = zoomFactor

# class ChatWindow():
class ChatViewer(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(ChatViewer, self).__init__(parent)
        # create all the widgets
        self.whatsapp = ChatWebView(self)
        self.slack = ChatWebView(self)
        self.telegram = ChatWebView(self) 
        self.messenger = ChatWebView(self)
        self.signal = ChatWebView(self)
        # load all messaging apps on various webviews.
        # self.whatsapp.load(QUrl("https://web.whatsapp.com/"))
        self.whatsapp.loadDevTools()
        self.slack.load(QUrl("https://slack.com/signin#/signin"))
        self.slack.loadDevTools()
        self.messenger.load(QUrl("https://www.messenger.com/"))
        self.messenger.loadDevTools()
        # self.telegram.load()
        # self.setElideMode(True)
        # add widgets to separate tabs.
        self.addTab(self.whatsapp.splitter, "WhatsApp")
        self.addTab(self.slack.splitter, "Slack")
        self.addTab(self.messenger.splitter, "Messenger")
        self.addTab(self.telegram.splitter, "Telegram")
        self.addTab(self.signal.splitter, "Signal")
        self.setCurrentIndex(0)
        # self.setStyleSheet(dash_calendar_style)

def test_chat():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    chatviewer = ChatViewer()
    # chatviewer.open("~/GUI/FileViewerTest")
    # fileviewer.saveScreenshot("fileviewer.html")
    chatviewer.show()
    app.exec()

if __name__ == '__main__':
    test_chat()