#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# the fig-dash music player is known as the "jukebox".
from fig_dash import FigDLoad
FigDLoad("fig_dash::ui::system::musicplayer")

import os
import time
import jinja2
import shutil
from typing import *
from pathlib import Path
from functools import partial
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.webview import DebugWebBrowser, DebugWebView
# from fig_dash.config import PDFJS_VIEWER_PATH
from fig_dash.ui import styleContextMenu, FigDMainWindow, DashRibbonMenu
# PyQt5 imports
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineSettings, QWebEngineContextMenuData
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence, QPalette
from PyQt5.QtCore import Qt, QSize, QFile, QFileInfo, QUrl, QMimeDatabase, pyqtSlot, pyqtSignal, QObject, QThread, QFileSystemWatcher
from PyQt5.QtWidgets import QShortcut, QWidget, QSplitter, QMainWindow, QApplication, QErrorMessage, QLabel, QLineEdit, QPlainTextEdit, QToolBar, QMenu, QToolButton, QSizePolicy, QFrame, QAction, QActionGroup, QLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect, QFileIconProvider, QSlider, QComboBox, QCompleter, QDirModel, QScrollArea

# JukeBox.
class MusicPlayerWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(MusicPlayerWidget, self).__init__(parent)
        