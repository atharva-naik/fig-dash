#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
from pathlib import Path
# fig-dash imports.
from fig_dash import FigD
from fig_dash.ui.browser import DebugWebView
# PyQt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QToolBar, QToolButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
# filweviewer widget.