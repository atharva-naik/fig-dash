#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import getpass
from typing import Union
# Qt imports.
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import QIcon, QFontMetrics
# from PyQt5.QtWebEngineWidgets import 
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl
from PyQt5.QtWidgets import QToolBar, QWidget, QAction


CONFIG_BOOKMARKS_PATH = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
if os.path.exists(CONFIG_BOOKMARKS_PATH):
    print(f"reading bookmarks config for chrome from {CONFIG_BOOKMARKS_PATH}")
else:
    print(f"didn't find bookmarks file at {CONFIG_BOOKMARKS_PATH}")
class BookmarkBar(QToolBar):
    bookmarkClicked = pyqtSignal(QUrl, str)

    def __init__(self, parent: Union[None, QWidget]=None):
        super(BookmarkBar, self).__init__(parent)
        self.actionTriggered.connect(self.bookmarkActionTriggered)
        self.bookmark_list = json.load(open(CONFIG_BOOKMARKS_PATH))["roots"]
        print(self.bookmark_list)
        print(f"found {len(self.bookmark_list)} bookmarks!")

    def setBookmarks(self, bookmarks):
        for bookmark in bookmarks:
            self.addBookmarkAction(
                bookmark["title"], 
                bookmark["url"]
            )

    def addBookmarkAction(self, title, url):
        bookmark = {
            "url": url,
            "title": title
        }
        fontMetrics = QFontMetrics(self.font())
        if bookmark not in self.bookmark_list:
            text = fontMetrics.elidedText(title, Qt.ElideRight, 150)
            action = self.addAction(text)
            action.setData(bookmark)
            self.bookmark_list.append(bookmark)

    @pyqtSlot(QAction)
    def bookmarkActionTriggered(self, action):
        bookmark = action.data()
        self.bookmarkClicked.emit(
            bookmark["url"], 
            bookmark["title"]
        )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.defaultUrl = QUrl()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        self.urlLe = QtWidgets.QLineEdit()
        self.urlLe.returnPressed.connect(self.onReturnPressed)
        self.favoriteButton = QtWidgets.QToolButton()
        self.favoriteButton.setIcon(QIcon("images/star.png"))
        self.favoriteButton.clicked.connect(self.addFavoriteClicked)

        toolbar = self.addToolBar("")
        toolbar.addWidget(self.urlLe)
        toolbar.addWidget(self.favoriteButton)

        self.addToolBarBreak()
        self.bookmarkToolbar = BookmarkBar()
        self.bookmarkToolbar.bookmarkClicked.connect(self.add_new_tab)
        self.addToolBar(self.bookmarkToolbar)
        self.readSettings()

    def onReturnPressed(self):
        self.tabs.currentWidget().setUrl(QUrl.fromUserInput(self.urlLe.text()))

    def addFavoriteClicked(self):
        loop = QtCore.QEventLoop()

        def callback(resp):
            setattr(self, "title", resp)
            loop.quit()

        web_browser = self.tabs.currentWidget()
        web_browser.page().runJavaScript("(function() { return document.title;})();", callback)
        url = web_browser.url()
        loop.exec_()
        self.bookmarkToolbar.addBookmarkAction(getattr(self, "title"), url)

    def add_new_tab(self, qurl=QUrl(), label='Blank'):
        web_browser = QtWebEngineWidgets.QWebEngineView()
        web_browser.setUrl(qurl)
        web_browser.adjustSize()
        web_browser.urlChanged.connect(self.updateUlrLe)
        index = self.tabs.addTab(web_browser, label)
        self.tabs.setCurrentIndex(index)
        self.urlLe.setText(qurl.toString())

    def updateUlrLe(self, url):
        self.urlLe.setText(url.toDisplayString())

    def readSettings(self):
        settings = QtCore.QSettings()
        self.defaultUrl = settings.value("defaultUrl", QUrl('http://www.google.com'))
        self.add_new_tab(self.defaultUrl, f'Hello {getpass.getuser()}!')
        bookmarks = settings.value("bookmarks", [])
        if bookmarks is None: bookmarks = []
        # print(settings.value("bookmarks", []))
        self.bookmarkToolbar.setBookmarks(bookmarks)

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue("defaultUrl", self.defaultUrl)
        settings.setValue("bookmarks", self.bookmarkToolbar.bookmark_list)

    def closeEvent(self, event):
        self.saveSettings()
        super(MainWindow, self).closeEvent(event)


if __name__ == '__main__':
    import sys

    QtCore.QCoreApplication.setOrganizationName("eyllanesc.org")
    QtCore.QCoreApplication.setOrganizationDomain("www.eyllanesc.com")
    QtCore.QCoreApplication.setApplicationName("MyApp")
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())