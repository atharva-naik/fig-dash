#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2
from typing import Union
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.browser.url.parse import UrlOrQuery
# PyQt5 imports
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QWidget, QToolBar, QLabel, QToolButton, QMainWindow, QSizePolicy, QLineEdit, QCompleter, QHBoxLayout, QAction, QGraphicsDropShadowEffect


dash_searchbar_style = jinja2.Template('''
QLineEdit {
    border: 0px;
    font-size: 16px;
    padding-top: 5px;
    padding-bottom: 5px;
    color: #fff; /* #ad3700; */
    /* background: qlineargradient(x1 : 1, y1 : 0, x2 : 0, y2: 0, stop: 0 #828282, stop: 0.5 #eee, stop: 1 #828282); */
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
    border-radius: {{ BORDER_RADIUS }};
}
QLabel {
    font-size: 16px;
}''')
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
        # share url accross devices (google account).
        self.shareDeviceAction = QAction()
        self.shareDeviceAction.setIcon(FigD.Icon("navbar/share_devices.svg"))
        self.addAction(self.shareDeviceAction, self.TrailingPosition)
        # get qr code for URL.
        self.qrCodeAction = QAction()
        self.qrCodeAction.setIcon(FigD.Icon("navbar/qrcode.svg"))
        self.addAction(self.qrCodeAction, self.TrailingPosition)
        # bookmark page.
        self.bookmarkAction = QAction()
        self.bookmarkAction.setIcon(FigD.Icon("navbar/bookmark.svg"))
        self.addAction(self.bookmarkAction, self.TrailingPosition)
        self.setStyleSheet(dash_searchbar_style.render(
            BORDER_RADIUS=14,
        ))
        self.setFixedHeight(28)
        self.label.move(30, 0)
        self.label.hide()
        self.textEdited.connect(self.formatQueryOrUrl)
        self.returnPressed.connect(self.search)
        # completion for search.
        self.completer = QCompleter()
        self.searchHistory = []
        self.setCompleter(self.completer)
        # apply glow effect.
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(2,0)
        glow_effect.setColor(QColor(235, 95, 52))
        # glow_effect.setColor(QColor(235, 156, 52))
        self.setGraphicsEffect(glow_effect)

    def search(self):
        url = UrlOrQuery(self.text())()
        self.searchHistory.append(url)
        self.completer = QCompleter(self.searchHistory)
        dash_navbar = self.parent()
        central_widget = dash_navbar.parent()
        dash_window = central_widget.parent()
        tabs = dash_window.tabs
        i = tabs.currentIndex()
        tabs.loadUrl(i, url)

    def formatQueryOrUrl(self, query_or_url: str):
        pass
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


dash_bar_btn_style = jinja2.Template('''
QToolButton {
    border: 0px;
    padding: 3px;
    border-radius: {{ (ICON_SIZE//2)+3 }};
    background: transparent;
}
QToolButton:hover {
    background: rgba(125, 125, 125, 0.7);
}''')
class DashBarBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, **kwargs):
        super(DashBarBtn, self).__init__(parent)
        icon = kwargs.get("icon")
        self.setIcon(FigD.Icon(icon))
        size = kwargs.get("size", (20, 20))
        self.setIconSize(QSize(*size))
        tip = kwargs.get("tip", "this is a tip.")
        self.setToolTip(tip)
        stylesheet = kwargs.get("style")
        self.setStyleSheet(stylesheet.render(
            ICON_SIZE=size[0],
        ))


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
        self.prevBtn = DashBarBtn(
            icon="navbar/prev.svg",
            tip="go to previous page in history",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.prevBtn)
        # go to next page in history.
        self.nextBtn = DashBarBtn(
            icon="navbar/next.svg",
            tip="go to next page in history",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.nextBtn)
        # reload page.
        self.reloadBtn = DashBarBtn(
            icon="navbar/reload.svg",
            tip="reload page",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.reloadBtn)
        # open homepage.
        self.homeBtn = DashBarBtn(
            icon="navbar/home.svg",
            tip="open homepage",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.homeBtn)
        # add search bar.
        self.searchbar = DashSearchBar(self)
        layout.addWidget(self.searchbar)
        self.setStyleSheet(dash_navbar_style.render())
        # extensions.
        self.extensionsBtn = DashBarBtn(
            icon="navbar/extensions.svg",
            tip="open extensions",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.extensionsBtn)
        # account.
        self.accountBtn = DashBarBtn(
            icon="navbar/account.png",
            tip="open account settings",
            style=dash_bar_btn_style,
            size=(24,24)
        )
        layout.addWidget(self.accountBtn)
        # history.
        self.historyBtn = DashBarBtn(
            icon="navbar/history.svg",
            tip="open search history",
            style=dash_bar_btn_style,
            size=(24,24)
        )
        layout.addWidget(self.historyBtn)
        # settings.
        self.settingsBtn = DashBarBtn(
            icon="navbar/more_settings.svg",
            tip="open browser settings",
            style=dash_bar_btn_style
        )
        layout.addWidget(self.settingsBtn)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.setFixedHeight(50)
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(2,2)
        glow_effect.setColor(QColor(235, 95, 52))
        self.setGraphicsEffect(glow_effect)
        # layout.addStretch(1)
    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget
        self.reloadBtn.clicked.connect(tabWidget.reloadUrl)
        self.nextBtn.clicked.connect(tabWidget.nextUrl)
        self.prevBtn.clicked.connect(tabWidget.prevUrl)
        self.homeBtn.clicked.connect(tabWidget.home)
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
