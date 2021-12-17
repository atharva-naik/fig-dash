#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Union, Tuple, List
# Qt imports.
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import Qt, QT_VERSION_STR
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget
# fig-dash imports.
from fig_dash.ui.tab import DashTabWidget
# from PyQt5.QtCore import QThread, QUrl, QDir, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QObject, QRect, QPoint
# from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QPainter
# from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QSplitter, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton, QGraphicsView, QGraphicsEffect, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect, QTextEdit
class DashWindow(QMainWindow):
    '''The main window for fig-dash.'''
    def __init__(self):
        super(DashWindow, self).__init__()
        self.tabs = DashTabWidget(self)
        self.tabs.addTab(QWidget(), "Untitled 1")
        self.setCentralWidget(self.tabs)