#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dock (hopefully like latte dock).
import json
import jinja2
from typing import Union
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.browser.url.parse import UrlOrQuery
# PyQt5 imports
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QPoint, QUrl, QEvent, QStringListModel, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QDockWidget, QLineEdit, QHBoxLayout


class DockSearchBar(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DockSearchBar, self).__init__(parent)
        self.setFixedHeight(35)
        self.setMaximumWidth(350)
        palette = self.palette()
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128,128,128))
        palette.setColor(QPalette.Base, QColor(29,29,29,255))
        palette.setColor(QPalette.Text, QColor(255,255,255))
        palette.setColor(QPalette.Window, QColor(29,29,29,255))
        palette.setColor(QPalette.WindowText, QColor(255,255,255,255))
        self.setPalette(palette)


class DockWidgetUI(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DockWidgetUI, self).__init__(parent)
        self.searchbar = DockSearchBar()
        # layout.
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        # populate layout.
        self.layout.addWidget(self.searchbar)
        # add widgets to layout.
        self.setLayout(self.layout)


class DashDockWidget(QDockWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashDockWidget, self).__init__("", parent)
        self.ui = DockWidgetUI()
        self.setWidget(self.ui)