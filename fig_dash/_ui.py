#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
import getpass
from typing import Union, Tuple, List
# Qt imports.
# from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR, QSize
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QSizePolicy
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.browser import PageInfo
from fig_dash.ui.tab import DashTabWidget
from fig_dash.ui.navbar import DashNavBar
from fig_dash.ui.titlebar import TitleBar
from fig_dash.ui.widget.ideas import IdeasWidget
from fig_dash.ui.widget.notifs import NotifsPanel
from fig_dash.ui.widget.weather import WeatherWidget
from fig_dash.ui.widget.floatmenu import FloatMenu
from fig_dash.ui.system.sysutils import SysUtilsBar
from fig_dash.ui.system.date_time import DashClock, DashCalendar
from fig_dash.ui.widget.richtexteditor import richtexteditor_style
# from PyQt5.QtCore import QThread, QUrl, QDir, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QObject, QRect, QPoint
# from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QPainter
# from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QSplitter, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton, QGraphicsView, QGraphicsEffect, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect, QTextEdit
dash_window_style = jinja2.Template('''
QMainWindow {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 2, stop : 0.1 #000, stop : 0.2 #292929, stop : 0.7 #917459, stop : 0.8 #cf6400);
}''')
dash_tabbar_style = jinja2.Template('''
QTabBar {
    border: 0px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 #eb5f34, stop : 0.6 #ebcc34);
}
QTabBar::close-button {
    border: 0px;
    background-repeat: no-repeat;
    background-position: center;
    subcontrol-position: right;
}
QTabBar::close-button:hover {
    background-color: rgba(235, 235, 235, 0.50);
    background-repeat: no-repeat;
    background-position: center;
    subcontrol-position: right;
}
QTabBar::tab {
    border: 0px;
    color: #292929;
    padding-top: 5px;
    padding-left: 9px;
    padding-right: 5px;
    padding-bottom: 5px;
    margin-left: 1px;
    margin-right: 1px;
    font-size: 18px;
    max-width: 300px;
}
QTabBar::tab:hover {
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop : 0.6 #eb5f34, stop: 0.9 #ebcc34);
}
QTabBar::tab:selected {
    color: #fff;
    border: 0px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
    padding-top: 5px;
    padding-left: 9px;
    padding-right: 5px;
    padding-bottom: 5px;
    margin-left: 1px;
    margin-right: 1px;
    font-size: 18px;
    font-weight: bold;
}''')
# all the splitters.
class DatetimeNotifsSplitter(QSplitter):
    '''Date, time and notifs panel contained in the splitter'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DatetimeNotifsSplitter, self).__init__(
            Qt.Vertical,
            parent=parent
        )
        self.clockWidget = DashClock(self)
        self.calendarWidget = DashCalendar(self)
        self.notifsPanel = NotifsPanel(self)
        # add all widgets.
        self.addWidget(self.clockWidget)
        self.addWidget(self.calendarWidget)
        self.addWidget(self.notifsPanel)

    def toggle(self):
        '''toggle visibility of the combined clock, calendar and notifs panel.'''
        if self.isVisible():
            self.hide()
        else: self.show()


class DashWindow(QMainWindow):
    '''The main window for fig-dash.'''
    def __init__(self, **kwargs):
        super(DashWindow, self).__init__()
        self.browsingHistory = []

        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        w = kwargs.get("w", 100)
        h = kwargs.get("h", 100)
        self.setGeometry(x, y, w, h)
        # self.firstResizeOver = False
        self.centralWidget = self.initCentralWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Dash Window")
        # print(kwargs.get('icon'))
        self.logo = QIcon(kwargs.get('icon'))
        # self.setWindowIcon(self.logo)

        maximize_by_default = kwargs.get("maximize_by_default", True)
        if maximize_by_default:
            self.showMaximized()
        # add title bar.
        self.titlebar = TitleBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.titlebar)
        # install event filter.
        self.installEventFilter(self)
        self.setStyleSheet(dash_window_style.render())

    def initTabWidget(self):
        tabs = DashTabWidget(self)
        tabs.connectWindow(self)
        tabs.openHome()
        # tabs.openUrl("https://github.com/atharva-naik")
        dummyBtn = QToolButton(self)
        dummyBtn.setStyleSheet("""
        QToolButton {
            border: 0px;
            background: transparent;
        }""")
        tabs.tabBar().setTabButton(0, QTabBar.RightSide, dummyBtn)
        # for i in range(5):
        #     tabs.openUrl("https://google.com")
        tabs.connectWindow(self)
        # tabs.openUrl("https://google.com")
        # tabs.openFile("/home/atharva/GUI/fig-dash/README.md")
        return tabs

    def initCentralWidget(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        # add tab widget.
        self.navbar = DashNavBar(self)
        self.tabs = self.initTabWidget()
        # top bar.
        self.topbar = QWidget()
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        self.topbar.setLayout(topLayout)
        # self.topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.topbar.setFixedHeight(35)
        # tabbar.
        self.tabbar = self.tabs.tabBar()
        self.tabbar.setStyleSheet(dash_tabbar_style.render())
        topLayout.addWidget(self.tabbar)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        topLayout.addWidget(spacer)
        # corner widget.
        topLayout.addWidget(self.tabs.cornerWidget())
        # topLayout.addWidget(self.tabs.dropdownBtn)
        # add search bar.
        self.navbar.setFixedHeight(30)
        self.navbar.connectTabWidget(self.tabs)
        # main horizontal splitter.
        self.h_split = QSplitter(Qt.Horizontal)
        # add tabwidget
        self.h_split.addWidget(self.tabs)
        # add notifications and datetime splitter.
        self.datetime_notifs_splitter = self.initDatetimeNotif()
        self.h_split.addWidget(self.datetime_notifs_splitter)
        self.h_split.setSizes([500,330,300])
        self.tabs.connectDropdown(self.h_split)
        # float menu widget
        self.floatmenu = FloatMenu(self.tabs)
        # self.floatmenu.hide()
        self.floatmenu.move(2,30)
        # system utilities bar.
        self.sysutilsbar = SysUtilsBar(self.tabs)
        # page info.
        self.page_info = PageInfo(self.tabs)
        # self.page_info.hide()
        # ideas widget.
        self.ideas = IdeasWidget(self.tabs)
        self.ideas.hide()
        # weather widget.
        self.weather = WeatherWidget(self.tabs)
        self.weather.move(100, 40)
        self.weather.hide()
        # self.h_split.setFixedHeight(500)
        # central vertical splitter.
        layout.insertWidget(0, self.h_split)
        layout.insertWidget(0, self.navbar)
        layout.insertWidget(0, self.topbar)
        self.floatmenu.connectWindow(self)
        # layout.addStretch(1)
        return centralWidget

    def setFlags(self, *flags):
        flag_map = {"frameless": "Qt.FramelessWindowHint", "ontop": "Qt.WindowStaysOnTopHint"}
        flag_str = "|".join([flag_map[flag] for flag in flags])
        code = f"self.setWindowFlags({flag_str})"
        exec(code)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self.page_info.move(self.width()-250, 50)
            self.ideas.move(80, self.height()-470)
            self.sysutilsbar.move(self.tabs.width()-50, 80)
            # if self.firstResizeOver:
            #     width = self.width() 
            #     self.tabs.dropdown.rePos(width=width, offset=170)
            # TODO: really ugly jugaad. Fix this.
        return super(DashWindow, self).eventFilter(obj, event)

    def moveEvent(self, event):
        super(DashWindow, self).moveEvent(event)
        dropdown = self.tabs.dropdownBtn.dropdown
        if dropdown:
            diff = event.pos() - event.oldPos()
            geo = dropdown.geometry()
            geo.moveTopLeft(geo.topLeft() + diff)
            dropdown.setGeometry(geo)

    def initDatetimeNotif(self):
        datetime_notifs_splitter = DatetimeNotifsSplitter(self)
        datetime_notifs_splitter.hide()
        datetime_notifs_splitter.notifsPanel.pushNotif(
            name="fig-dash",
            icon=FigD.icon("logo.png"),
            msg=f"Hi <b>{getpass.getuser()}</b>! Click <a href='https://github.com/atharva-naik/fig-dash' style='color: #269e92;'>here</a> to get started with <b>fig-dash</b>."
        )
        datetime_notifs_splitter.notifsPanel.pushNotif(
            name="Hire Me?",
            icon=FigD.icon("me.jpeg"),
            msg=f"If you like what you see, and want to hire me, check out my <a href='https://www.linkedin.com/in/atharva-naik-112888190/' style='color: #269e92;'>LinkedIn profile</a>."
        )

        return datetime_notifs_splitter