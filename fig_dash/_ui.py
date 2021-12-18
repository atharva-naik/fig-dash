#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Union, Tuple, List
# Qt imports.
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import Qt, QT_VERSION_STR
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget, QVBoxLayout
# fig-dash imports.
from fig_dash.ui.tab import DashTabWidget
from fig_dash.ui.titlebar import TitleBar
# from PyQt5.QtCore import QThread, QUrl, QDir, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QObject, QRect, QPoint
# from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QPainter
# from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QSplitter, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton, QGraphicsView, QGraphicsEffect, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect, QTextEdit
class DashWindow(QMainWindow):
    '''The main window for fig-dash.'''
    def __init__(self, **kwargs):
        super(DashWindow, self).__init__()

        self.centralWidget = self.initCentralWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Dash Window")

        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        w = kwargs.get("w", 100)
        h = kwargs.get("h", 100)
        self.setGeometry(x, y, w, h)
        
        maximize_by_default = kwargs.get("maximize_by_default", True)
        if maximize_by_default:
            self.showMaximized()
        # add title bar.
        self.titlebar = TitleBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.titlebar)

    def initTabWidget(self):
        tabs = DashTabWidget(self)
        tabs.openFile("/home/atharva/GUI/fig-dash/README.md")

        return tabs

    def initCentralWidget(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        # add tab widget.
        self.tabs = self.initTabWidget()
        layout.addWidget(self.tabs)

        return centralWidget

    def setFlags(self, *flags):
        flag_map = {"frameless": "Qt.FramelessWindowHint", "ontop": "Qt.WindowStaysOnTopHint"}
        flag_str = "|".join([flag_map[flag] for flag in flags])
        code = f"self.setWindowFlags({flag_str})"
        # print(code)
        exec(code)