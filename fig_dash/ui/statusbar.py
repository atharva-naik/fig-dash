#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSignal, QFileInfo, Qt, QPoint, QMimeDatabase, QUrl, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolBar, QToolButton, QLabel, QFileIconProvider, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QTabBar, QPushButton, QGraphicsDropShadowEffect
# fig-dash imports.
from fig_dash.assets import FigD


class StatusBar(QToolBar):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(StatusBar, self).__init__(parent)

    # def 