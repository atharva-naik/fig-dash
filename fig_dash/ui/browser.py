#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtGui import QIcon, QFontMetrics
from typing import Union
from pprint import pprint
from requests.exceptions import MissingSchema
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl
from PyQt5.QtWidgets import QToolBar, QWidget, QAction
# fig_dash
from ..utils import QFetchIcon
from fig_dash.assets import FigD


scrollbar_style = '''*::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}    
*::-webkit-scrollbar-track {
    background-color: rgba(235, 235, 235, 0.8);
}
*::-webkit-scrollbar-track:hover {
    background-color: rgba(29, 29, 29, 0.4);
}
*::-webkit-scrollbar-thumb {
    background-color: #292929;
}
*::-webkit-scrollbar-thumb:hover {
    background: rgb(235,95,52);
    background: linear-gradient(0deg, rgba(235,95,52,1) 40%, rgba(235,204,52,1) 94%);;
}
*::-webkit-scrollbar-corner {
    background-color: transparent;
    /* background: rgba(235, 235, 235, 0.1); */
}'''
class Browser(QWebEngineView):
    def __init__(self, parent: Union[None, QWidget]):
        super(Browser, self).__init__(parent)
        self.currentZoomFactor = 1.25
        self.setZoomFactor(self.currentZoomFactor)
    # def pageIconCallback(self, html: str):
    #     from bs4 import BeautifulSoup
    #     soup = BeautifulSoup(html, features="html.parser")
    #     icon_links = soup.findAll("link", **{"rel": "icon"})
    #     icon_path = None
    #     is_svg = False
    #     for icon in icon_links:
    #         icon_path = icon["href"]
    #         if icon["type"] == "image/svg+xml": 
    #             is_svg = True
    #             break
    #     if icon_path:
    #         self.pageIcon = QFetchIcon(
    #             icon_path, 
    #             is_svg
    #         )
    #         pprint(icon_path)
    def append(self, url: Union[str, QUrl]):
        '''append url to browsing history.'''
        try:
            browsingHistory = self.window.browsingHistory
        except AttributeError as e:
            print("not connected to a DashWindow")
            return
        try:
            browsingHistory.append(url.toString())
        except AttributeError as e:
            browsingHistory.append(url)
        print(f"\x1b[31;1m{browsingHistory}\x1b[0m")

    def updateTabTitle(self):
        self.append(self.url())
        try:
            i = self.tabWidget.currentIndex()
            self.loadFinished.connect(
                lambda: self.tabWidget.setTabTitle(
                    i, self.page.title()
                )
            )
        except AttributeError as e:
            print("not connected to a TabWidget")

    def setUrl(self, url):
        self.append(url)
        super(Browser, self).setUrl(url)

    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget 
        self.urlChanged.connect(self.updateTabTitle)
        try: self.window = tabWidget.dash_window
        except AttributeError as e:
            print("TabWidget not connected to DashWindow") 

    def setScrollbar(self, style: str=scrollbar_style):
        code = f'''Style = `{scrollbar_style}`
let newStyle = document.createElement('style');
newStyle.innerHTML = Style
document.head.appendChild(newStyle);'''
        self.page().runJavaScript(code)

    def iconSetCallback(self, html: str):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, features="html.parser")
        icon_links = soup.findAll("link", **{"rel": "icon"})
        icon_path, is_svg = None, False
        for icon in icon_links:
            icon_path = icon["href"]
            if icon.get("type")=="image/svg+xml": is_svg = True; break
        if icon_path:
            try:
                pageIcon = QFetchIcon(icon_path, is_svg)
            except MissingSchema:
                pageIcon = FigD.Icon("browser.svg")    
        else:
            pageIcon = FigD.Icon("browser.svg")
        self.tabs.setTabIcon(self.i, pageIcon)

    def setIcon(self, tabs, i: int):
        self.i = i
        self.tabs = tabs
        self.page().toHtml(self.iconSetCallback)
    # def fetchIcon(self):
    #     self.page().toHtml(self.pageIconCallback)
# class MainWindow(QWidget):
#     def __init__(self, parent=None):
#         super(QWidget, self).__init__(parent)
#         self.defaultUrl = QUrl()


#         toolbar = self.addToolBar("")
#         toolbar.addWidget(self.urlLe)
#         toolbar.addWidget(self.favoriteButton)

#         self.addToolBarBreak()
#         self.bookmarkToolbar = BookmarkBar()
#         self.bookmarkToolbar.bookmarkClicked.connect(self.add_new_tab)
#         self.addToolBar(self.bookmarkToolbar)
#         self.readSettings()

#     def onReturnPressed(self):
#         self.tabs.currentWidget().setUrl(QUrl.fromUserInput(self.urlLe.text()))

#     def addFavoriteClicked(self):
#         loop = QtCore.QEventLoop()

#         def callback(resp):
#             setattr(self, "title", resp)
#             loop.quit()

#         web_browser = self.tabs.currentWidget()
#         web_browser.page().runJavaScript("(function() { return document.title;})();", callback)
#         url = web_browser.url()
#         loop.exec_()
#         self.bookmarkToolbar.addBookmarkAction(getattr(self, "title"), url)

#     def add_new_tab(self, qurl=QUrl(), label='Blank'):
#         web_browser = QtWebEngineWidgets.QWebEngineView()
#         web_browser.setUrl(qurl)
#         web_browser.adjustSize()
#         web_browser.urlChanged.connect(self.updateUlrLe)
#         index = self.tabs.addTab(web_browser, label)
#         self.tabs.setCurrentIndex(index)
#         self.urlLe.setText(qurl.toString())

#     def updateUlrLe(self, url):
#         self.urlLe.setText(url.toDisplayString())

#     def readSettings(self):
#         settings = QtCore.QSettings()
#         self.defaultUrl = settings.value("defaultUrl", QUrl('http://www.google.com'))
#         self.add_new_tab(self.defaultUrl, f'Hello {getpass.getuser()}!')
#         bookmarks = settings.value("bookmarks", [])
#         if bookmarks is None: bookmarks = []
#         # print(settings.value("bookmarks", []))
#         self.bookmarkToolbar.setBookmarks(bookmarks)

#     def saveSettings(self):
#         settings = QtCore.QSettings()
#         settings.setValue("defaultUrl", self.defaultUrl)
#         settings.setValue("bookmarks", self.bookmarkToolbar.bookmark_list)

#     def closeEvent(self, event):
#         self.saveSettings()
#         super(MainWindow, self).closeEvent(event)