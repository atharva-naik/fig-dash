#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bar containing bookmarks and extensions.
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
from typing import Union, Tuple
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize, QObject
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsDropShadowEffect, QTextEdit, QShortcut
# fig_dash
from ..utils import QFetchIcon
from fig_dash.assets import FigD
from fig_dash.api.browser.extensions import ExtensionManager
from fig_dash.api.browser.extensions import BookmarksManager

class ExtensionLoader(QObject):
    '''worker to load extensions.'''
    def __init__(self, manager):
        self.manager = manager # reference to extension manager.
    # def 

class ExtrasBar(QWidget):
    '''bookmarks + extensions'''
    def __init__(self, parent: Union[QWidget, None]=None):
        super(ExtrasBar, self).__init__(parent)
        self.extension_manager = ExtensionManager()
        self.bookmarks_manager = BookmarksManager()

    def loadExtensions(self):
        pass

    def loadBookmarks(self):
        pass