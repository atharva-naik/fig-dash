#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fig_dash import FigDLoad
FigDLoad("fig_dash::_ui")

import jinja2
import getpass
from typing import *
# Qt imports.
# from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR, QSize 
from PyQt5.QtWidgets import QApplication, QSplitter, QMainWindow, QWidget, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QSizePolicy, QSpacerItem, QShortcut, QTabWidget
# fig-dash imports.
from fig_dash.assets import FigD

# from fig_dash.ui.widget.floatmenu import FloatMenu

# from PyQt5.QtCore import QThread, QUrl, QDir, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QObject, QRect, QPoint
# from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QPainter
# from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QSplitter, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton, QGraphicsView, QGraphicsEffect, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect, QTextEdit
dash_window_style = jinja2.Template('''
QMainWindow {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 2, stop : 0.1 #000, stop : 0.2 #292929, stop : 0.7 #917459, stop : 0.8 #cf6400); */
    background: url('''+FigD.wallpapers(0)+''');
    background-repeat: no-repeat; 
    background-position: center;
}''')
# qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(235, 95, 52, 220), stop : 0.6 rgba(235, 204, 52, 220));
dash_tabbar_style = jinja2.Template('''
QTabBar {
    border: 0px;
    background: transparent;
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
    color: #fff;

    margin-left: 1px;
    margin-right: 1px;

    padding-top: 5px;
    padding-left: 9px;
    padding-right: 5px;
    padding-bottom: 5px;

    font-size: 17px;
    font-family: 'Be Vietnam Pro', sans-serif;
    max-width: 300px;
    background: #000;
}
QTabBar::tab:hover {
    color: #fff;
    background: #323232;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 200), stop : 0.3 rgba(191, 54, 54, 220), stop : 0.6 rgba(235, 95, 52, 220), stop: 0.9 rgba(235, 204, 52, 220)); */
}
QTabBar::tab:selected {
    color: #eee;
    border: 0px;
    background: #323232;
    font-weight: bold;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e4852c, stop : 0.143 #e4822d, stop : 0.286 #e4802f, stop : 0.429 #e47d30, stop : 0.571 #e47b32, stop : 0.714 #e47833, stop : 0.857 #e47635, stop : 1.0 #e47336); */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
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
class WrapperWidget(QWidget):
    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()


class AppCloseButton(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(AppCloseButton, self).__init__(parent)
        self.setIcon(FigD.Icon("close.png"))
        self.setStyleSheet("""
        QToolButton {
            border: 0px;
            background: transparent;
        }""")

    def enterEvent(self, event):
        self.setIcon(FigD.Icon("close-active.png"))
        super(AppCloseButton, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon("close.png"))
        super(AppCloseButton, self).leaveEvent(event)


class DatetimeSplitter(QSplitter):
    '''Date, time and notifs panel contained in the splitter'''
    def __init__(self, parent: Union[None, QWidget]=None):
        from fig_dash.ui.system.datetime import DashClock, DashCalendar
        super(DatetimeSplitter, self).__init__(
            Qt.Vertical,
            parent=parent
        )
        self.clockWidget = DashClock(self)
        self.calendarWidget = DashCalendar(self)
        # add all widgets.
        self.addWidget(self.clockWidget)
        self.addWidget(self.calendarWidget)
        # self.addWidget(self.notifsPanel)
    def toggle(self):
        '''toggle visibility of the combined clock, calendar and notifs panel.'''
        if self.isVisible():
            self.hide()
        else: self.show()


class DashWindow(QMainWindow):
    '''The main window for fig-dash.'''
    def __init__(self, **kwargs):
        from fig_dash.ui.dock import DashDockWidget
        from fig_dash.ui.shortcutbar import ShortcutBar
        # imports for installed apps. 
        from fig_dash.ui.apps.screenshot import DashScreenshotUI

        super(DashWindow, self).__init__()
        self.browsingHistory = []
        # self.setAttribute(Qt.WA_TranslucentBackground)
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        w = kwargs.get("w", 100)
        h = kwargs.get("h", 100)
        self.setGeometry(x, y, w, h)
        self.statusBar().setStyleSheet("""
        QStatusBar {
            color: #eb5f34;
            font-size: 16px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        }""")
        self.statusBar().setMaximumHeight(30)
        from fig_dash.ui.titlebar import TitleBar
        self.titlebar = TitleBar(self)
        self.centralWidget = self.initCentralWidget(**kwargs)
        self.tabs.connectWindow(self)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Dash Window")
        # self.setWindowOpacity(0.92)
        # print(kwargs.get('icon'))
        self.logo = QIcon(kwargs.get('icon'))
        # self.setWindowIcon(self.logo)
        maximize_by_default = kwargs.get("maximize_by_default", True)
        if maximize_by_default:
            self.showMaximized()
            
        self.titlebar.connectTabWidget(self.tabs)
        # add shortcuts sidebar.
        self.shortcutbar = ShortcutBar(self)
        self.shortcutbar.connectTabs(self.tabs)
        self.sysutilsbar.connectTitleBar(self.titlebar)
        self.tabs.connectTitleBar(self.titlebar)
        self.addToolBar(Qt.TopToolBarArea, self.titlebar)
        self.addToolBar(Qt.LeftToolBarArea, self.shortcutbar)
        self.addToolBar(Qt.LeftToolBarArea, self.shortcutbar.app_launcher)
        self.addToolBar(Qt.LeftToolBarArea, self.shortcutbar.utils_launcher)

        self.dock = DashDockWidget()
        self.dock.setParent(self.tabs)
        self.dock.move(300, 300)
        self.dock.show()
        # self.dock.setGeometry(100, 100, 500, 70)
        self.shortcutbar.utils_launcher.connectWindow(self)
        # install event filter.
        self.installEventFilter(self)
        self.setStyleSheet(dash_window_style.render())
        # shortcuts.
        self.FnF1 = QShortcut(Qt.Key_F1, self)
        self.FnF1.activated.connect(self.toggleMuteVolSlider)
        self.FnF2 = QShortcut(Qt.Key_F2, self)
        self.FnF2.activated.connect(self.decVolSlider)
        self.FnF3 = QShortcut(Qt.Key_F3, self)
        self.FnF3.activated.connect(self.incVolSlider)
        # connect the screenshotting UI.
        app = QApplication.instance()
        screen_rect = app.desktop().screenGeometry()
        w, h = screen_rect.width()//2, screen_rect.height()//2
        self.screenshot_ui = DashScreenshotUI(app=app)
        self.screenshot_ui.move(w, h)
        # connect a screenshot Win+S for launching the screenshot UI.
        self.WinS = QShortcut(QKeySequence("Ctrl+Shift+P"), self)
        self.WinS.activated.connect(self.screenshot_ui.show)
        # add spacers.
        spacer1 = QWidget()
        spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.menu.connectWindow(self)
        # connect close button of the first tab with application close.
        self.statusBar().addWidget(spacer1)
        self.statusBar().addWidget(self.menu.fileviewer.statusbar)
        self.statusBar().addWidget(self.menu.cm_editor.statusbar)
        self.statusBar().addWidget(self.menu.browser_statusbar)
        self.statusBar().addWidget(spacer2)

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
            print(f"\x1b[31;1m_ui.invVolSlider:\x1b[0m {e}")
            self.initVolumeSlider()

    def toggleMuteVolSlider(self):
        '''pop out the volume slider'''
        print("toggling mute.")

    def decVolSlider(self):
        '''pop out the volume slider'''
        try:
            if not self.volume_slider.isVisible():
                self.volume_slider.show()
            self.volume_slider.increase()
        except AttributeError as e:
            print(f"\x1b[31;1m_ui.decVolSlider:\x1b[0m {e}")
            self.initVolumeSlider()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            self.titlebar.fullscreenBtn.toggle()

    def initTabWidget(self, open_home=True, **kwargs):
        from fig_dash.ui.tab import DashTabWidget
        tabs = DashTabWidget(self)
        tabs.partialConnectWindow(self)
        if open_home:
            tabs.openHome()
            tabs.tabBar().tabButton(
                0, QTabBar.RightSide
            ).clicked.connect(
                self.close
            )
            # dummyBtn = AppCloseButton(self)
            # dummyBtn.clicked.connect(
            #     self.close
            # )
            # tabs.tabBar().setTabButton(
            #     0, QTabBar.RightSide, 
            #     dummyBtn
            # )
        else: print("\x1b[32;1mopen_home=False\x1b[0m")
        # for i in range(5):
        #     tabs.openUrl("https://google.com")
        # tabs.connectWindow(self)
        # tabs.openUrl("https://google.com")
        # tabs.openFile("/home/atharva/GUI/fig-dash/README.md")
        return tabs
        # if self.titlebar

    def initCentralWidget(self, **kwargs):
        from fig_dash.ui.menu import DashMenu
        from fig_dash.ui.navbar import DashNavBar
        from fig_dash.ui.widget.ideas import IdeasWidget
        from fig_dash.ui.system.sysutils import SysUtilsBar
        from fig_dash.ui.widget.weather import WeatherWidget

        self.menu = DashMenu(self, **kwargs)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        centralWidget.customName = "ui._ui.DashWindow::centralWidget"
        # add tab widget.
        self.navbar = DashNavBar(self)
        self.tabs = self.initTabWidget(**kwargs)
        print(self.tabs.children())
        # self.tabs.setTabBarAutoHide(True)
        # self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.installEventFilter(self)
        
        # top bar.
        self.topbar = QWidget()
        topLayout = QHBoxLayout()
        topLayout.setSpacing(5)
        topLayout.setContentsMargins(0, 0, 0, 0)
        self.topbar.setObjectName("TopBar")
        self.topbar.setLayout(topLayout)
        self.topbar.setStyleSheet("""
        /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e4852c, stop : 0.143 #e47f2c, stop : 0.286 #e57a2d, stop : 0.429 #e5742d, stop : 0.571 #e56e2e, stop : 0.714 #e56830, stop : 0.857 #e46231, stop : 1.0 #e45c33); */
        QWidget#TopBar {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.7), stop : 0.143 rgba(22, 22, 22, 0.7), stop : 0.286 rgba(27, 27, 27, 0.7), stop : 0.429 rgba(32, 32, 32, 0.7), stop : 0.571 rgba(37, 37, 37, 0.7), stop : 0.714 rgba(41, 41, 41, 0.7), stop : 0.857 rgba(46, 46, 46, 0.7), stop : 1.0 rgba(51, 51, 51, 0.7));
        }""")
        # self.topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.topbar.setFixedHeight(35)
        # tabbar.
        self.tabbar = self.tabs.tabBar()
        self.tabbar.setStyleSheet(dash_tabbar_style.render())
        topLayout.addWidget(self.tabbar)
        # corner widget.
        # self.tabs.cornerWidget(            
        # ).setSizePolicy(
        #     QSizePolicy.Expanding, 
        #     QSizePolicy.Fixed
        # )
        cornerWidget = self.tabs.tabCornerWidget
        plusBtn = self.tabs.plusBtn
        topLayout.addWidget(plusBtn, 0, Qt.AlignVCenter)
        topLayout.addStretch(1)
        topLayout.addWidget(cornerWidget, 0, Qt.AlignVCenter)
        # add search bar.
        self.navBarWrapper = QWidget()# WrapperWidget()
        navBarLayout = QHBoxLayout()
        navBarLayout.setContentsMargins(0, 0, 0, 0)
        navBarLayout.setSpacing(0)
        self.navBarWrapper.setObjectName("NavBarWrapper")
        self.navBarWrapper.setStyleSheet("""
        QWidget#NavBarWrapper {
            background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 rgba(17, 17, 17, 0.7), stop : 0.143 rgba(22, 22, 22, 0.7), stop : 0.286 rgba(27, 27, 27, 0.7), stop : 0.429 rgba(32, 32, 32, 0.7), stop : 0.571 rgba(37, 37, 37, 0.7), stop : 0.714 rgba(41, 41, 41, 0.7), stop : 0.857 rgba(46, 46, 46, 0.7), stop : 1.0 rgba(51, 51, 51, 0.7));
        }""")
        self.navBarWrapper.setFixedHeight(38)
        self.navbar.connectTabWidget(self.tabs)
        navBarLayout.addWidget(self.navbar)
        self.navBarWrapper.setLayout(navBarLayout)
        # main horizontal splitter.
        self.h_split = QSplitter(Qt.Horizontal)
        # add tabwidget
        self.tabs_stacked_widget = self.tabs.children()[0]
        self.h_split.addWidget(self.tabs)
        # add notifications and datetime splitter.
        self.datetime_notifs_splitter = self.initDatetime()
        self.notifsPanel = self.initNotifs(self.tabs)
        self.h_split.addWidget(self.datetime_notifs_splitter)
        self.h_split.setSizes([800,200,200])
        self.tabs.connectDropdown(self.h_split)

        # hide the empty space that was once taken up by the tabbar.
        # print(self.tabbar)
        # print(self.tabs.tabBar())
        # print(self.tabbar == self.tabs.tabBar())
        # print(self.tabbar.parent())
        # print(self.tabs.tabBar().parent())
        # print(self.tabbar.parent() == self.tabs.tabBar().parent())
        # self.tabs.tabBar().hide()
        # float menu widget
        # self.floatmenu = FloatMenu(self.tabs)
        # self.floatmenu.hide()
        # self.floatmenu.move(2,30)
        # system utilities bar.
        self.sysutilsbar = SysUtilsBar(self.tabs)
        self.sysutilsbar.hide()
        # page info.
        from fig_dash.ui.webview import PageInfo
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
        layout.insertWidget(0, self.menu) 
        layout.insertWidget(0, self.navBarWrapper)
        layout.insertWidget(0, self.topbar)       
        # self.floatmenu.connectWindow(self)
        # layout.addStretch(1)
        return centralWidget

    def toggleNavBar(self):
        # needed to do this because using WrapperWidget instance for navBarWrapper led to background styling being ignored.
        if self.navBarWrapper.isVisible():
            self.navBarWrapper.hide()
        else: self.navBarWrapper.show()

    def setFlags(self, *flags):
        flag_map = {"frameless": "Qt.FramelessWindowHint", "ontop": "Qt.WindowStaysOnTopHint"}
        flag_str = "|".join([flag_map[flag] for flag in flags])
        code = f"self.setWindowFlags({flag_str})"
        exec(code)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self.ideas.move(80, self.height()-470)
            self.page_info.move(self.width()-270, 50)
            self.notifsPanel.move(self.tabs.width()-self.notifsPanel.width()-100, self.tabs.height()-self.notifsPanel.height()-5)
            self.sysutilsbar.move(self.tabs.width()-100, 50)
            # if self.firstResizeOver: width = self.width() self.tabs.dropdown.rePos(width=width, offset=170)
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
        self.shortcutbar.setMetaBarPos()
        self.shortcutbar.morePagesBtn.setPos()
        self.shortcutbar.moreSocialBtn.setPos()
        self.shortcutbar.moreSystemBtn.setPos()
        dock_width = self.width()/2-350 #(self.width() - self.shortcutbar.width())//2
        dock_height = self.height()-250
        try: 
            self.dock.move(dock_width, dock_height)
            self.tabs.currentWidget().browser.searchPanel.setPos()
        except Exception as e: 
            print(f"\x1b[31;1m_ui.resizeEvent:\x1b[0m {e}")
        super(DashWindow, self).resizeEvent(event)

    def initNotifs(self, tabWidget: QWidget=None):
        from fig_dash.ui.widget.notifs import NotifsPanel
        # notifs panel.
        notifsPanel = NotifsPanel(tabWidget)
        notifsPanel.move(100, 20)
        # notifsPanel.hide()
        notifsPanel.pushNotif(
            name="fig-dash",
            icon=FigD.icon("logo.svg"),
            msg=f"Hi <b>{getpass.getuser()}</b>! Click <a href='https://github.com/atharva-naik/fig-dash' style='color: #269e92;'>here</a> to get started with <b>fig-dash</b>."
        )
        notifsPanel.pushNotif(
            name="Hire Me?",
            icon=FigD.icon("me.jpeg"),
            msg=f"If you like what you see, and want to hire me, check out my <a href='https://www.linkedin.com/in/atharva-naik-112888190/' style='color: #269e92;'>LinkedIn profile</a>."
        )

        return notifsPanel

    def initDatetime(self):
        datetime_splitter = DatetimeSplitter(self)
        datetime_splitter.hide()

        return datetime_splitter