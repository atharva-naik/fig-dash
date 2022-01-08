#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
from pprint import pprint
from typing import Union, Tuple
from requests.exceptions import MissingSchema
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QMimeDatabase, Qt, QUrl, QSize
from PyQt5.QtWidgets import QToolBar, QToolButton, QSplitter, QLabel, QWidget, QAction, QVBoxLayout, QApplication, QSizePolicy, QGraphicsDropShadowEffect
# fig_dash
from ..utils import QFetchIcon
from fig_dash.assets import FigD

# HOME_URL = "file:///tmp/fig_dash.rendered.content.html"
class DevToolsBtn(QToolButton): 
    def __init__(self, parent: Union[None, QWidget]=None, 
                size: Tuple[int, int]=(23,23)):
        super(DevToolsBtn, self).__init__(parent)
        self.inactive_icon = "browser/dev_tools.svg"
        self.active_icon = "browser/dev_tools_active.svg"
        self.setIcon(FigD.Icon(self.inactive_icon))
        self.setIconSize(QSize(*size))
        self.setToolTip("open devtools (inspect)")
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon))
        super(DevToolsBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(DevToolsBtn, self).leaveEvent(event)


class DebugWebView(QWebEngineView):
    def __init__(self, dev_tools_zoom=1.35):
        super(DebugWebView, self).__init__()
        self.dev_view = QWebEngineView()
        self.devToolsBtn = DevToolsBtn(self)
        self.dev_tools_zoom = dev_tools_zoom
        self.devToolsBtn.clicked.connect(self.toggleDevTools)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self)
        self.splitter.addWidget(self.dev_view)
        self.splitter.setSizes([500, 300])
        self.dev_view.hide()
        self.dev_view.loadFinished.connect(self.setDevToolsZoom)

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        # print(dir(self.menu))
        self.menu.setStyleSheet("background: #292929; color: #fff;")
        self.menu.addAction(FigD.Icon("qrcode.svg"), "Create QR code for this page")
        self.menu.actions()[0].setIcon(FigD.Icon("qrcode.svg"))
        self.menu.addSeparator()
        self.menu.addAction(FigD.Icon("trans.svg"), "Translate to English")
        self.menu.popup(event.globalPos())

    def alert(self, msg: str):
        self.page().runJavaScript(f"alert(`{msg}`);")

    def setDevToolsZoom(self):
        self.dev_view.setZoomFactor(self.dev_tools_zoom)

    def toggleDevTools(self):
        if self.dev_view.isVisible():
            self.dev_view.hide()
        else:
            self.dev_view.show()

    def loadDevTools(self):
        self.dev_view.load(QUrl("http://0.0.0.0:5000/"))
        self.page().setDevToolsPage(self.dev_view.page())

        
scrollbar_style = '''*::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
*::-webkit-scrollbar-track:hover {
    background: rgba(29, 29, 29, 0.4);
}    
*::-webkit-scrollbar-track {
    /* background-color: rgba(235, 235, 235, 0.8); */
    background: linear-gradient(0deg, rgba(235,95,52,0.8) 0%, rgba(235,204,52,1) 94%);
}
*::-webkit-scrollbar-thumb {
    background-color: #292929;
}
*::-webkit-scrollbar-thumb:hover {
    background: rgb(235,95,52);
    background: linear-gradient(0deg, rgba(235,95,52,1) 40%, rgba(235,204,52,1) 94%);
}
*::-webkit-scrollbar-corner {
    background-color: transparent;
    /* background: rgba(235, 235, 235, 0.1); */
}'''
selection_style = '''
::selection {
	color: #fff;
    background-color: rgb(235,95,52);
}
::selection:window-inactive {
	color: #000;
    background-color: rgb(235,204,52);
}'''
class PageInfo(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(PageInfo, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)
        # page info.
        self.label = QLabel("Page Info")
        self.label.setStyleSheet('''
        QLabel {
            border: 0px;
            padding: 10px;
            color: #eb5f34;
            font-size: 20px;
            font-weight: bold;
        }''')
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        # word count of page.
        self.word_count = QToolButton(self)
        self.word_count.setIcon(FigD.Icon("time_to_read.svg"))
        self.word_count.setIconSize(QSize(20,20))
        self.word_count.setText(" 0 words")
        self.word_count.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.word_count.setToolTip("word count of webpage.")
        self.word_count.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.word_count.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.addWidget(self.word_count)
        # time taken to read.
        self.time_to_read = QToolButton(self)
        self.time_to_read.setIcon(FigD.Icon("word_count.svg"))
        self.time_to_read.setIconSize(QSize(20,20))
        self.time_to_read.setText(" 0 mins")
        self.time_to_read.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.time_to_read.setToolTip("time taken to read webpage.")
        self.time_to_read.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.time_to_read.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.addWidget(self.time_to_read)
        self.layout.addStretch(1)

        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        wrapper = QWidget()
        wrapper.setObjectName("wrapper")
        wrapper.setStyleSheet('''
        QWidget#wrapper {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }''')
        wrapper.setLayout(self.layout)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.word_count.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            padding: 5px;
        }''')
        self.time_to_read.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            padding: 5px;
        }''')

        self.setGraphicsEffect(glow_effect)
        self.setFixedWidth(150)
        layout.addWidget(wrapper)
        self.setLayout(layout)
        # self.setFixedWidth(100)
    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()
    
    def update(self, word_count: Union[int, None]):
        if word_count is None:
            word_count = 0
        '''assuming average human adult reads at 200 wpm'''
        self.word_count.setText(f" {word_count} words")
        self.time_to_read.setText(f" {word_count // 200} mins")
        # self.setFixedHeight(100)
class Browser(QWebEngineView):
    def __init__(self, parent: Union[None, QWidget], zoomFactor: float=1.25):
        super(Browser, self).__init__(parent)
        self.mime_database = QMimeDatabase()
        self.historyIndex = 0
        self.browsingHistory = []
        self.currentZoomFactor = zoomFactor
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
        try: url = url.toString()
        except AttributeError as e: pass
        # store in local tab browsing history.
        if len(self.browsingHistory) > 0 and self.browsingHistory[-1] == url:
            self.browsingHistory.append(url)
            self.historyIndex = len(self.browsingHistory)-1
        try:
            if len(self.dash_window.browsingHistory) > 0 and self.dash_window.browsingHistory[-1] == url:
                return
            else:
                self.dash_window.browsingHistory.append(url)
                print(f"\x1b[31;1m{self.dash_window.browsingHistory}\x1b[0m")
        except AttributeError as e:
            print("not connected to a DashWindow")
            return    

    def prevInHistory(self):
        self.historyIndex -= 1
        self.historyIndex = max(0, self.historyIndex)
        self.back()

    def nextInHistory(self):
        self.historyIndex += 1
        self.historyIndex = min(len(self.browsingHistory)-1, self.historyIndex)
        self.forward()

    def dragEnterEvent(self, e):
        from pathlib import Path
        from pprint import pprint

        filename = e.mimeData().text().strip()
        filename = filename.replace("file://", "")
        mimetype = self.mime_database.mimeTypeForFile(filename).name()
        print(f"dragEvent for {'folder' if os.path.isdir(filename) else 'file'}: {filename}, with mimetype: {mimetype}")
        if os.path.isdir(filename):
            # case when item being opened is actually a folder.
            self.dash_window.tabs.openWidget(
                widget=self.dash_window.menu.fileviewer,
                icon=FigD.Icon("system/fileviewer/folder.svg"),
                title=filename, 
            )
            self.dash_window.menu.fileviewer.connectWindow(self.dash_window)
            self.dash_window.menu.fileviewer.open(filename)
        else:
            super(Browser, self).dragEnterEvent(e)

    def updateTabTitle(self):
        try:
            self.dash_window.navbar.searchbar.setText(
                self.url().toString()
            )
        except AttributeError as e:
            print("not connected to DashWindow") 
        self.append(self.url())
        try:
            # change title ofthe tab that contains this browser only.
            if self != self.tabWidget.currentWidget(): return
            i = self.tabWidget.currentIndex()
            if i < 0: return
            print(f"updating title for tab-{i}")
            self.loadFinished.connect(
                lambda: self.tabWidget.setupTabForBrowser(
                    i=i, browser=self,
                )
            )
        except AttributeError as e:
            print("not connected to a TabWidget")

    def setUrl(self, url):
        self.append(url)
        super(Browser, self).setUrl(url)

    def setWordCount(self):
        code = '''
        function calculateWordCount(text) {
            const wordsArr = text.trim().split(" ")
            return wordsArr.filter(word => word !== "").length
        }
        calculateWordCount(document.body.textContent);
        '''
        self.page().runJavaScript(code, self._word_count_callback)

    def _word_count_callback(self, word_count: int):
        try:
            self.dash_window.page_info.update(word_count)
        except AttributeError as e:
            print("TabWidget not connected to DashWindow") 

    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget 
        self.urlChanged.connect(self.updateTabTitle)
        try: self.dash_window = tabWidget.dash_window
        except AttributeError as e:
            print("TabWidget not connected to DashWindow") 

    def setScrollbar(self, style: str=scrollbar_style):
        code = f'''Style = `{scrollbar_style}`
newScrollbarStyle = document.createElement('style');
newScrollbarStyle.innerHTML = Style
document.head.appendChild(newScrollbarStyle);'''
        self.page().runJavaScript(code)

    def setSelectionStyle(self, style: str=selection_style):
        code = f'''Style = `{style}`
newSelectStyle = document.createElement('style');
newSelectStyle.innerHTML = Style
document.head.appendChild(newSelectStyle);
'''
        self.page().runJavaScript(code)

    # def drop

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
def test_page_info():
    FigD("/home/atharva/GUI/fig-dash/resources")
    import sys
    app = QApplication(sys.argv)
    page_info = PageInfo()
    page_info.show()
    app.exec()


if __name__ == "__main__":
    test_page_info()