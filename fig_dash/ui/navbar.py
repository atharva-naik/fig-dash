#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import jinja2
import requests
import urllib.parse
from typing import Union
from functools import partial
from json.decoder import JSONDecodeError
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.browser.url.parse import UrlOrQuery
# PyQt5 imports
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QUrl, QEvent, QStringListModel, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QToolBar, QMenu, QLabel, QToolButton, QMainWindow, QTabWidget, QSizePolicy, QLineEdit, QCompleter, QHBoxLayout, QAction, QGraphicsDropShadowEffect


dash_searchbar_style = jinja2.Template('''
QLineEdit {
    border: 0px;
    font-size: 17px;
    font-family: Ubuntu;
    padding-top: 3px;
    padding-bottom: 3px;
    color: #fff; /* #ad3700; */
    selection-background-color: #eb5f34;
    /* background: qlineargradient(x1 : 1, y1 : 0, x2 : 0, y2: 0, stop: 0 #828282, stop: 0.5 #eee, stop: 1 #828282); */
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
    border-radius: {{ BORDER_RADIUS }};
}
QLabel {
    font-size: 16px;
}''')
class GoogleAutoCompleteThread(QThread):
    searched = pyqtSignal(str)
    def __init__(self):
        super(GoogleAutoCompleteThread, self).__init__()


class GoogleAutoCompleteWorker(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)
    def __init__(self):
        super(GoogleAutoCompleteWorker, self).__init__()
        self.query_format = "http://suggestqueries.google.com/complete/search?client=firefox&q={}"
        
    @pyqtSlot()
    def completeQuery(self, query: str=""): 
        query_enc = urllib.parse.quote_plus(query)
        url = self.query_format.format(query_enc)
        response = requests.get(url).text
        self.progress.emit(response)
        # self.finished.emit(response)
# def getGoogleAutoCompletion(query: str) -> list:
#     """[summary]
#     ## Google AutoCompletion querying function 
#     very rudimentary version of Google's autocompletion feature. (missing error handling/not tested for edge cases)
#     Args:
#         query (str): [The query for which autcompletion results need to be retrieved]

#     Returns:
#         list: [suggestions returned by the API]
#     """
#     import json
#     import requests
#     import urllib.parse

#     query_enc = urllib.parse.quote_plus(query)
#     url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={query_enc}"
#     response = json.loads(requests.get(url).text)
#     # return requests.get(url).text
#     return response[1]
class DashSearchBar(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashSearchBar, self).__init__(parent)
        self.label = QLabel("")
        self.label.setParent(self)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        # view site info.
        self.siteInfoAction = QAction()
        self.siteInfoAction.setIcon(FigD.Icon("navbar/lock.svg"))
        self.addAction(self.siteInfoAction, self.LeadingPosition)
        # bookmark page.
        self.bookmarkAction = QAction()
        self.bookmarkAction.setIcon(FigD.Icon("navbar/bookmark.svg"))
        self.addAction(self.bookmarkAction, self.TrailingPosition)
        self.bookmarkAction.triggered.connect(self.toggleBookmark)
        # app download.
        self.appDownloadAction = QAction()
        self.appDownloadAction.setIcon(FigD.Icon("navbar/download_app.svg"))
        self.addAction(self.appDownloadAction, self.TrailingPosition)
        self.appDownloadAction.setVisible(False)
        # get qr code for URL.
        self.qrCodeAction = QAction()
        self.qrCodeAction.setIcon(FigD.Icon("navbar/qrcode.svg"))
        self.addAction(self.qrCodeAction, self.TrailingPosition)
        # share url accross devices (google account).
        self.shareDeviceAction = QAction()
        self.shareDeviceAction.setIcon(FigD.Icon("navbar/share_devices.svg"))
        self.addAction(self.shareDeviceAction, self.TrailingPosition)
        # clipboard permission.
        self.clipboardAction = QAction()
        self.clipboardAction.setIcon(FigD.Icon("navbar/clipboard.svg"))
        self.addAction(self.clipboardAction, self.TrailingPosition)
        self.clipboardAction.setVisible(False)
        # location permission.
        self.locationAction = QAction()
        self.locationAction.setIcon(FigD.Icon("navbar/location.svg"))
        self.addAction(self.locationAction, self.TrailingPosition)
        self.locationAction.setVisible(False)
        # notifications permission.
        self.notificationsAction = QAction()
        self.notificationsAction.setIcon(FigD.Icon("navbar/notifications.svg"))
        self.addAction(self.notificationsAction, self.TrailingPosition)
        self.notificationsAction.setVisible(False)
        # camera permission.
        self.cameraAction = QAction()
        self.cameraAction.setIcon(FigD.Icon("navbar/camera.svg"))
        self.addAction(self.cameraAction, self.TrailingPosition)
        self.cameraAction.setVisible(False)
        # mic permission.
        self.micAction = QAction()
        self.micAction.setIcon(FigD.Icon("navbar/mic.svg"))
        self.addAction(self.micAction, self.TrailingPosition)
        self.micAction.setVisible(False)
        # terminal mode.
        self.terminalAction = QAction()
        self.terminalAction.setIcon(FigD.Icon("navbar/terminal.svg"))
        self.addAction(self.terminalAction, self.TrailingPosition)
        self.terminalAction.triggered.connect(self.toggleTerminal)

        self.setStyleSheet(dash_searchbar_style.render(
            BORDER_RADIUS=16,
        ))
        self.setFixedHeight(28)
        self.label.move(30, 0)
        self.label.hide()
        self.textEdited.connect(self.updateCompleter)
        self.returnPressed.connect(self.search)
        # completion for search.
        self.suggestions = []
        self.autoCompleteThread = GoogleAutoCompleteThread()
        self.autoCompleteWorker = GoogleAutoCompleteWorker()
        self.autoCompleteWorker.moveToThread(
            self.autoCompleteThread
        )
        self.autoCompleteWorker.progress.connect(
            self.onAutoCompletion
        )
        self.autoCompleteWorker.finished.connect(
            self.autoCompleteThread.quit
        )
        self.autoCompleteWorker.finished.connect(
            self.autoCompleteWorker.deleteLater
        )
        self.autoCompleteThread.finished.connect(
            self.autoCompleteThread.deleteLater
        )
        self.autoCompleteThread.start()
        self.autoCompleteThread.searched.connect(
            self.autoCompleteWorker.completeQuery
        )
        self.completer = QCompleter(self.suggestions)
        # self.completer.setStyleSheet("""font-family: 'Be Vietnam Pro', sans-serif; color: #fff; background: #000;""")
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # self.completer.setFilterMode(Qt.MatchContains)
        self.searchHistory = []
        self.setCompleter(self.completer)

    def updateCompleter(self):
        # self.autoCompleteThread.started.connect(
        #     lambda: self.autoCompleteWorker.completeQuery(
        #         self.text()
        #     )
        # )
        import time
        s = time.time()
        self.autoCompleteThread.searched.emit(
            self.text()
        )
        t = time.time()-s
        print(f"issued autcomplete request for {self.text()} in {t}s")
# https://developer.mozilla.org/en-US/docs/Web/OpenSearch
    def setText(self, text: str):
        super(DashSearchBar, self).setText(text)
        self.setCursorPosition(0)

    def toggleTerminal(self):
        '''terminalize current tab.'''
        try: tabWidget = self.tabWidget
        except Exception as e:          
            print(f"\x1b[31;1mnavbar.toggleTerminal:\x1b[0m {e}"); return
        if tabWidget is None: return
        browser = tabWidget.currentWidget().browser
        try:
            if browser.isTerminalized():
                tabWidget.unterminal()
                self.terminalAction.setIcon(FigD.Icon("navbar/terminal.svg"))
            else:
                tabWidget.terminal()
                self.terminalAction.setIcon(FigD.Icon("navbar/terminal_active.svg"))
        except Exception as e: 
            print(f"\x1b[31;1mnavbar.toggleTerminal:\x1b[0m {e}")

    def toggleBookmark(self):
        '''toggle bookmark status of the current browser page/tab.'''
        try: tabWidget = self.tabWidget
        except Exception as e: 
            print(f"\x1b[31;1mnavbar.toggleBookmark:\x1b[0m {e}")
            return
        if tabWidget is None: return
        browser = tabWidget.currentWidget().browser
        try:
            if browser.isBookmarked():
                browser.setBookmark(False)
                self.bookmarkAction.setIcon(FigD.Icon("navbar/bookmark.svg"))
            else:
                browser.setBookmark(True)
                self.bookmarkAction.setIcon(FigD.Icon("navbar/bookmark_active.svg"))
        except Exception as e: 
            print(f"\x1b[31;1mnavbar.toggleBookmark:\x1b[0m {e}")

    def glow(self):
        '''apply glow effect.'''
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(30)
        glow_effect.setOffset(0,0)
        glow_effect.setColor(QColor(235, 95, 52))
        # glow_effect.setColor(QColor(235, 156, 52))
        self.setGraphicsEffect(glow_effect)

    def unglow(self):
        '''remove glow effect'''
        self.setGraphicsEffect(None)

    def mousePressEvent(self, event):
        '''select text on click'''
        super(DashSearchBar, self).mousePressEvent(event)
        if not self.hasSelectedText():
            self.setCursorPosition(0)
            self.selectAll()

    def focusInEvent(self, event):
        super(DashSearchBar, self).focusInEvent(event)
        self.glow()

    def focusOutEvent(self, event):
        super(DashSearchBar, self).focusOutEvent(event)
        self.unglow()
        # self.setCursorPosition(0)
    def setUrl(self, url: Union[QUrl, str]):
        if isinstance(url, QUrl):
            url = url.toString(QUrl.FullyEncoded)
        # print("is this a temporary url?", url.startswith(FigD.TempURLPath))
        if url == "file:///tmp/fig_dash.rendered.content.html": 
            self.setText("")
            self.setPlaceholderText("Search Google or type a URL")
        elif url.startswith(FigD.TempURLPath):
            self.setText("")
            self.setPlaceholderText("Type a terminal command")
        else:
            self.setText(url)
        self.setCursorPosition(0)

    def search(self):
        dash_navbar = self.parent()
        central_widget = dash_navbar.parent()
        dash_window = central_widget.parent()
        tabs = dash_window.tabs
        i = tabs.currentIndex()
        try:
            browser = tabs.currentWidget().browser
        except Exception as e:
            print(f"\x1b[31;1mnavbar.search:\x1b[0m {e}")
            return
        if browser.isTerminalized():
            cmd = self.text()
            self.setText("")
            browser.execTerminalCommand(cmd)
            self.setPlaceholderText("Type a terminal command")
        else:
            text = self.text()
            qurl = UrlOrQuery(text)()
            print(qurl.toString())
            self.searchHistory.append(qurl.toString())
            tabs.loadUrlForIndex(i, qurl)
        # self.completer = QCompleter(self.searchHistory)
    def onAutoCompletion(self, json_str: str):
        try:
            self.suggestions += json.loads(json_str)[1]
        except JSONDecodeError: 
            return # self.suggestions  = [] 
        # ["abc", "bcd", "cde", "def"]
        self.model = QStringListModel()
        self.model.setStringList(self.suggestions)
        self.completer.setModel(self.model)
        # print("autocompleting")
        # self.completer.setModel(QStringListModel())
    # def formatQueryOrUrl(self, query_or_url: str):
    #     pass
        # qou = UrlOrQuery(query_or_url)
        # if qou.isUrl: 
        #     if qou.protocol == "http": 
        #         qou.set_colors("red", "black", "grey")
        #     else: 
        #         qou.set_colors("green", "black", "grey")
        #     self.label.show()
        # else: 
        #     self.label.hide()
        # self.label.setText(str(qou))
    def resizeEvent(self, event):
        self.label.setFixedHeight(self.height())
        self.label.setFixedWidth(self.width())
        super(DashSearchBar, self).resizeEvent(event)


dash_bar_btn_style = jinja2.Template("""
QToolButton {
    border: 0px;
    padding: 3px;
    border-radius: {{ (ICON_SIZE//2)+3 }};
    background: transparent;
}
QToolButton:hover {
    background: rgba(125, 125, 125, 0.7);
}
QMenu {
    color: #fff;
    font-family: 'Be Vietnam Pro', sans-serif;
    /* background: rgba(29,29,29,0.8); */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(0,0,0,0.9), stop : 0.6 rgba(29,29,29,0.9));
}
QMenu:selected  {
    color: #292929;
    font-weight: bold;
    background: #eb5f34; /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
}
QMenu::separator {
    background: #484848;
}""")
class DashNavBarBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, **kwargs):
        super(DashNavBarBtn, self).__init__(parent)
        icon = kwargs.get("icon")
        self.icon_path = icon
        stem, ext = os.path.splitext(icon)
        self.icon_disabled_path = stem + "_disabled" + ext
        self.setIcon(FigD.Icon(icon))
        size = kwargs.get("size", (20, 20))
        self.setIconSize(QSize(*size))
        tip = kwargs.get("tip", "this is a tip.")
        self.setToolTip(tip)
        stylesheet = kwargs.get("style")
        self.setStyleSheet(stylesheet.render(
            ICON_SIZE=size[0],
        ))

    def setEnabled(self, value: bool):
        if value:
            self.setIcon(FigD.Icon(self.icon_path))
        else:
            self.setIcon(FigD.Icon(self.icon_disabled_path))
        super(DashNavBarBtn, self).setEnabled(value)


class ReloadBtn(DashNavBarBtn):
    def __init__(self, *args, **kwargs):
        super(ReloadBtn, self).__init__(*args, **kwargs)
        self.menu = QMenu(self)
        self.mode = "reload"
        self.hardReload = self.menu.addAction(
            FigD.Icon("navbar/reload.svg"), 
            "hard refresh"
        )
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def connectTabWidget(self, tabWidget: QWidget):
        self.tabWidget = tabWidget
        self.clicked.connect(self.response)

    def response(self) -> None:
        """_summary_
        The default response is to stop loading the page if the page is currently loading or reload the page if it has already been loaded.
        """
        i = self.tabWidget.currentIndex()
        if self.mode == "reload":
            self.tabWidget.reloadUrl(i)
        else:
            self.tabWidget.stopLoading(i)

    def setStopMode(self, value: bool=True):
        if value:
            self.mode = "stop"
            self.setIcon(FigD.Icon("navbar/stop.svg"))
        else: 
            self.mode = "reload"
            self.setIcon(FigD.Icon("navbar/reload.svg"))

    def onContextMenu(self, point):
        self.menu.exec_(self.mapToGlobal(point))


class BackNavBtn(DashNavBarBtn):
    def __init__(self, *args, **kwargs):
        super(BackNavBtn, self).__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def connectTabWidget(self, tabWidget: QTabWidget):
        self.tabWidget = tabWidget

    def showHistory(self):
        print("full history")

    def goToItem(self, item):
        print(item.title())
        self.tabWidget.goToItem(item)

    def onContextMenu(self, point):
        self.historyActions = []
        try:
            currentWidget = self.tabWidget.currentWidget()
            browser = currentWidget.browser
            history = browser.history()
            currentIndex = history.currentItemIndex()
            self.menu = QMenu(self)
            items = []
            for i, item in enumerate(history.items()):
                if i >= currentIndex: continue
                items.append(item)
            for i, item in enumerate(items[::-1]):
                action = self.menu.addAction(
                    FigD.Icon("browser.svg"), 
                    item.title()
                )
                action.triggered.connect(partial(
                    self.goToItem, item
                ))
                self.historyActions.append(action)
            self.menu.addSeparator()
            self.showHistoryAction = self.menu.addAction(FigD.Icon("navbar/history.svg"), "Show full history")
            self.showHistoryAction.triggered.connect(self.showHistory)
            self.menu.exec_(self.mapToGlobal(point))
        except Exception as e:
            print("\x1b[31;1mnavbar.BackNavBtn.onContextMenu:\x1b[0m", e)


class NextNavBtn(BackNavBtn):
    def onContextMenu(self, point):
        self.historyActions = []
        try:
            currentWidget = self.tabWidget.currentWidget()
            browser = currentWidget.browser
            history = browser.history()
            currentIndex = history.currentItemIndex()
            self.menu = QMenu(self)
            for i, item in enumerate(history.items()):
                if i <= currentIndex: continue
                action = self.menu.addAction(
                    FigD.Icon("browser.svg"), 
                    item.title()
                )
                action.triggered.connect(partial(self.goToItem, item))
                self.historyActions.append(action)
            self.menu.addSeparator()
            self.showHistoryAction = self.menu.addAction(FigD.Icon("navbar/history.svg"), "Show full history")
            self.showHistoryAction.triggered.connect(self.showHistory)
            self.menu.exec_(self.mapToGlobal(point))
        except Exception as e:
            print("\x1b[31;1mnavbar.NextNavBtn.onContextMenu:\x1b[0m", e)


dash_navbar_style = jinja2.Template('''
QWidget {
    background: #b1b1b1;
}''')
class DashNavBar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashNavBar, self).__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)
        # go to previous page in history.
        self.btns = []
        self.prevBtn = BackNavBtn(
            icon="navbar/prev.svg",
            tip="go to previous page in history",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.prevBtn)
        self.btns.append(self.prevBtn)
        # go to next page in history.
        self.nextBtn = NextNavBtn(
            icon="navbar/next.svg",
            tip="go to next page in history",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.nextBtn)
        self.btns.append(self.nextBtn)
        # reload page.
        self.reloadBtn = ReloadBtn(
            icon="navbar/reload.svg",
            tip="reload page",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.reloadBtn)
        self.btns.append(self.reloadBtn)
        # open homepage.
        self.homeBtn = DashNavBarBtn(
            icon="navbar/home.svg",
            tip="open homepage",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.homeBtn)
        self.btns.append(self.homeBtn)
        # add search bar.
        self.searchbar = DashSearchBar(self)
        self.searchbar.setFixedHeight(33)
        layout.addWidget(self.searchbar)
        self.setStyleSheet(dash_navbar_style.render())
        # extensions.
        self.extensionsBtn = DashNavBarBtn(
            icon="navbar/extensions.svg",
            tip="open extensions",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.extensionsBtn)
        self.btns.append(self.extensionsBtn)
        # account.
        self.accountBtn = DashNavBarBtn(
            icon="navbar/account.png",
            tip="open account settings",
            style=dash_bar_btn_style,
            size=(24,24)
        )
        layout.addWidget(self.accountBtn)
        self.btns.append(self.accountBtn)
        # history.
        self.historyBtn = DashNavBarBtn(
            icon="navbar/history.svg",
            tip="open search history",
            style=dash_bar_btn_style,
            size=(24,24)
        )
        layout.addWidget(self.historyBtn)
        self.btns.append(self.historyBtn)
        # settings.
        self.settingsBtn = DashNavBarBtn(
            icon="navbar/more_settings.svg",
            tip="open browser settings",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.settingsBtn)
        self.btns.append(self.settingsBtn)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.setFixedHeight(50)
        # appy glow to all buttons
        for btn in self.btns:
            self.applyGlow(btn, color=(225,225,225))
        # layout.addStretch(1)
    def applyGlow(self, widget, color=(235, 95, 52)):
        '''for applying glow effect to buttons'''
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(10)
        glow_effect.setOffset(0,0)
        glow_effect.setColor(QColor(*color))
        widget.setGraphicsEffect(glow_effect)

    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget
        self.searchbar.tabWidget = tabWidget
        self.reloadBtn.connectTabWidget(tabWidget)
        self.nextBtn.clicked.connect(tabWidget.nextUrl)
        self.prevBtn.clicked.connect(tabWidget.prevUrl)
        self.homeBtn.clicked.connect(tabWidget.home)
        self.nextBtn.connectTabWidget(tabWidget)
        self.prevBtn.connectTabWidget(tabWidget)
# class DashSearchBar(QWidget):
#     def __init__(self, parent: Union[None, QWidget]=None):
#         super(DashSearchBar, self).__init__(parent)
#         self.layout = QHBoxLayout()
#         self.layout.setContentsMargins(0, 0, 0, 0)
#         self.layout.setSpacing(0)
#         self.setLayout(self.layout)
#         # view site info.
#         self.siteInfoBtn = QToolButton(self)
#         self.siteInfoBtn.setIcon(FigD.Icon("navbar/lock.svg"))
#         self.siteInfoBtn.setIconSize(QSize(16,16))
#         self.siteInfoBtn.setFixedHeight(30)
#         self.layout.addWidget(self.siteInfoBtn)
#         # search area.
#         self.searchArea = QTextEdit("0")
#         self.searchArea.setFixedHeight(30)
#         self.searchArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.searchArea.setLineWrapMode(QTextEdit.NoWrap)
#         self.layout.addWidget(self.searchArea)
#         # share url accross devices (google account).
#         self.shareDeviceBtn = QToolButton(self)
#         self.shareDeviceBtn.setIcon(FigD.Icon("navbar/share_devices.svg"))
#         self.shareDeviceBtn.setFixedHeight(30)
#         self.shareDeviceBtn.setIconSize(QSize(20,20))
#         self.layout.addWidget(self.shareDeviceBtn)
#         # get qr code for URL.
#         self.qrCodeBtn = QToolButton(self)
#         self.qrCodeBtn.setIcon(FigD.Icon("navbar/qrcode.svg"))
#         self.qrCodeBtn.setFixedHeight(30)
#         self.qrCodeBtn.setIconSize(QSize(20,20))
#         self.layout.addWidget(self.qrCodeBtn)
#         # bookmark page.
#         self.bookmarkBtn = QToolButton(self)
#         self.bookmarkBtn.setIcon(FigD.Icon("navbar/bookmark.svg"))
#         self.bookmarkBtn.setIconSize(QSize(20,20))
#         self.bookmarkBtn.setFixedHeight(30)
#         self.layout.addWidget(self.bookmarkBtn)
#         self.setStyleSheet(dash_searchbar_style.render(
#             BORDER_RADIUS=15,
#         ))
