#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::apps::container")
import os
import sys
import time
import jinja2
from typing import *
from pathlib import Path
# fig-dash imports.
from fig_dash.assets import FigD
# from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
from fig_dash.ui import wrapFigDWindow, styleContextMenu, FigDAppContainer, FigDShortcut
# PyQt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence, QPalette
from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSlot, pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QToolBar, QMenu, QToolButton, QSizePolicy, QFrame, QAction, QActionGroup, QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect, QScrollArea

# launch application from desktop file.
def test_container():
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    icon="fig.svg"
    accent_color = "white"
    container = QWidget.createWindowContainer()
    window = wrapFigDWindow(container, icon=icon, width=800,
                            height=600, accent_color=accent_color,
                            name="fileviewer")
    app.exec()