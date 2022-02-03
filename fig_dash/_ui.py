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
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QSizePolicy, QStatusBar, QShortcut
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.menu import DashMenu
from fig_dash.ui.browser import PageInfo
from fig_dash.ui.tab import DashTabWidget
from fig_dash.ui.navbar import DashNavBar
from fig_dash.ui.titlebar import TitleBar
from fig_dash.ui.widget.ideas import IdeasWidget
from fig_dash.ui.widget.notifs import NotifsPanel
from fig_dash.ui.widget.weather import WeatherWidget
from fig_dash.ui.widget.floatmenu import FloatMenu
from fig_dash.ui.system.sysutils import SysUtilsBar
from fig_dash.ui.system.datetime import DashClock, DashCalendar
from fig_dash.ui.shortcut_sidebar import ShortcutSidebar
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
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(235, 95, 52, 220), stop : 0.6 rgba(235, 204, 52, 220));
}
QTabBar::close-button {
    background: url("/home/atharva/GUI/fig-dash/resources/icons/close.png");
    background-repeat: no-repeat;
    background-position: center;
}
QTabBar::close-button:hover {
    background: url("/home/atharva/GUI/fig-dash/resources/icons/close-active.png");
    background-repeat: no-repeat;
    background-position: center;
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
    font-size: 17px;
    font-family: 'Be Vietnam Pro', sans-serif;
    max-width: 300px;
}
QTabBar::tab:hover {
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 200), stop : 0.3 rgba(191, 54, 54, 220), stop : 0.6 rgba(235, 95, 52, 220), stop: 0.9 rgba(235, 204, 52, 220));
}
QTabBar::tab:selected {
    color: #fff;
    border: 0px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220));
    padding-top: 5px;
    padding-left: 9px;
    padding-right: 5px;
    padding-bottom: 5px;
    margin-left: 1px;
    margin-right: 1px;
    font-size: 17px;
    font-weight: bold;
}''')
# #eb5f34, #ebcc34
# #a11f53, #eb5f34
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
        self.statusBar().setStyleSheet("""
        QStatusBar {
            color: #fff;
            font-size: 16px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
            background: #000;
        }""")
        self.statusBar().setMaximumHeight(20)
        # self.firstResizeOver = False
        self.centralWidget = self.initCentralWidget(**kwargs)
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
        self.titlebar.connectTabWidget(self.tabs)
        # add shortcuts sidebar.
        self.shortcut_sidebar = ShortcutSidebar(self)
        self.shortcut_sidebar.connectTabs(self.tabs)
        self.sysutilsbar.connectTitleBar(self.titlebar)
        self.tabs.connectTitleBar(self.titlebar)
        self.addToolBar(Qt.TopToolBarArea, self.titlebar)
        self.addToolBar(Qt.LeftToolBarArea, self.shortcut_sidebar)
        # install event filter.
        self.installEventFilter(self)
        self.setStyleSheet(dash_window_style.render())
        # shortcuts.
        self.FnF2 = QShortcut(Qt.Key_F2, self)
        self.FnF2.activated.connect(self.decVolSlider)
        self.FnF3 = QShortcut(Qt.Key_F3, self)
        self.FnF3.activated.connect(self.incVolSlider)

    def initVolumeSlider(self):
        from fig_dash.ui.system.audio import VolumeSlider
        print("initialized volume slider")
        self.volume_slider = VolumeSlider()
        self.volume_slider.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Popup)
        self.volume_slider.setGeometry(1400, 100, 500, 100)
        self.volume_slider.show()

    def incVolSlider(self):
        '''pop out the volume slider'''
        try:
            if not self.volume_slider.isVisible():
                self.volume_slider.show()
            self.volume_slider.decrease()
        except AttributeError as e:
            print(e)
            self.initVolumeSlider()

    def decVolSlider(self):
        '''pop out the volume slider'''
        try:
            if not self.volume_slider.isVisible():
                self.volume_slider.show()
            self.volume_slider.increase()
        except AttributeError as e:
            print(e)
            self.initVolumeSlider()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            self.titlebar.fullscreenBtn.toggle()

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

    def initCentralWidget(self, **kwargs):
        self.menu = DashMenu(self, **kwargs)
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
        topLayout.setSpacing(0)
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
        self.navbar.setFixedHeight(40)
        self.navbar.connectTabWidget(self.tabs)
        # main horizontal splitter.
        self.h_split = QSplitter(Qt.Horizontal)
        # add tabwidget
        self.h_split.addWidget(self.tabs)
        # add notifications and datetime splitter.
        self.datetime_notifs_splitter = self.initDatetimeNotif()
        self.h_split.addWidget(self.datetime_notifs_splitter)
        self.h_split.setSizes([800,200,200])
        self.tabs.connectDropdown(self.h_split)
        # float menu widget
        self.floatmenu = FloatMenu(self.tabs)
        self.floatmenu.hide()
        self.floatmenu.move(2,30)
        # system utilities bar.
        self.sysutilsbar = SysUtilsBar(self.tabs)
        self.sysutilsbar.hide()
        # page info.
        self.page_info = PageInfo(self.tabs)
        self.page_info.hide()
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
        layout.insertWidget(0, self.menu)
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
            self.page_info.move(self.width()-270, 50)
            self.ideas.move(80, self.height()-470)
            self.sysutilsbar.move(self.tabs.width()-100, 50)
            # if self.firstResizeOver:
            #     width = self.width() 
            #     self.tabs.dropdown.rePos(width=width, offset=170)
            # TODO: really ugly jugaad. Fix this.
        return super(DashWindow, self).eventFilter(obj, event)
    # def moveEvent(self, event):
    #     super(DashWindow, self).moveEvent(event)
    #     dropdown = self.tabs.dropdownBtn.dropdown
    #     if dropdown:
    #         diff = event.pos() - event.oldPos()
    #         geo = dropdown.geometry()
    #         geo.moveTopLeft(geo.topLeft() + diff)
    #         dropdown.setGeometry(geo)
    def resizeEvent(self, event):
        self.shortcut_sidebar.setPos()
        self.shortcut_sidebar.morePagesBtn.setPos()
        self.shortcut_sidebar.moreSocialBtn.setPos()
        self.shortcut_sidebar.moreSystemBtn.setPos()
        try: 
            self.tabs.currentWidget().browser.searchPanel.setPos()
        except Exception as e: print(e)
        super(DashWindow, self).resizeEvent(event)

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