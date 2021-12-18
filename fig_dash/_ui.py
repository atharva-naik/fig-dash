#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union, Tuple, List
# Qt imports.
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
# fig-dash imports.
from fig_dash.ui.tab import DashTabWidget
from fig_dash.ui.navbar import DashNavBar
from fig_dash.ui.titlebar import TitleBar
# from PyQt5.QtCore import QThread, QUrl, QDir, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QObject, QRect, QPoint
# from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QPainter
# from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QSplitter, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton, QGraphicsView, QGraphicsEffect, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect, QTextEdit
dash_window_style = jinja2.Template('''
QMainWindow {
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 2, stop : 0.1 #000, stop : 0.2 #292929, stop : 0.7 #917459, stop : 0.8 #cf6400);
}''')
dash_tabbar_style = jinja2.Template('''
QTabBar {
    border: 0px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 #eb5f34, stop : 0.6 #ebcc34);
}
/* QTabBar::close-button {
    background: url();
    background-repeat: no-repeat;
    background-position: center;
    subcontrol-position: right;
    border-radius: 12px;
}
QTabBar::close-button:hover {
    background: url();
    background-color: rgba(235, 235, 235, 0.50);
    background-repeat: no-repeat;
    background-position: center;
    subcontrol-position: right;
} */
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
class DashWindow(QMainWindow):
    '''The main window for fig-dash.'''
    def __init__(self, **kwargs):
        super(DashWindow, self).__init__()

        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        w = kwargs.get("w", 100)
        h = kwargs.get("h", 100)
        self.setGeometry(x, y, w, h)
        self.firstResizeOver = False

        self.centralWidget = self.initCentralWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Dash Window")
        
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
        tabs.openFile("/home/atharva/GUI/fig-dash/README.md")
        # tabs.openFile("/home/atharva/GUI/fig-dash/requirements.txt")
        # tabs.openFile("/home/atharva/GUI/fig-dash/setup.py")

        return tabs

    def initCentralWidget(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        # add tab widget.
        self.tabs = self.initTabWidget()
        # top bar.
        self.topbar = QWidget()
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        self.topbar.setLayout(topLayout)
        # tabbar.
        self.tabbar = self.tabs.tabBar()
        self.tabbar.setStyleSheet(dash_tabbar_style.render())
        topLayout.addWidget(self.tabbar)
        topLayout.addStretch(1)
        # corner widget.
        self.tabbar_dropdown = self.tabs.cornerWidget()
        topLayout.addWidget(self.tabbar_dropdown)

        layout.addWidget(self.topbar)
        # add search bar.
        self.navbar = DashNavBar(self)
        layout.addWidget(self.navbar)
        layout.addWidget(self.tabs)

        return centralWidget

    def setFlags(self, *flags):
        flag_map = {"frameless": "Qt.FramelessWindowHint", "ontop": "Qt.WindowStaysOnTopHint"}
        flag_str = "|".join([flag_map[flag] for flag in flags])
        code = f"self.setWindowFlags({flag_str})"
        # print(code)
        exec(code)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            if self.firstResizeOver:
                width = self.width() 
                self.tabs.dropdown.rePos(
                    width=width,
                    offset=170,
                )
            # TODO: really ugly jugaad. Fix this.
            if self.firstResizeOver == False:
                self.firstResizeOver = True
        return super(DashWindow, self).eventFilter(obj, event)

    def moveEvent(self, event):
        super(DashWindow, self).moveEvent(event)
        dropdown = self.tabs.dropdownBtn.dropdown
        if dropdown:
            diff = event.pos() - event.oldPos()
            geo = dropdown.geometry()
            geo.moveTopLeft(geo.topLeft() + diff)
            dropdown.setGeometry(geo)