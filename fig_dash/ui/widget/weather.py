#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union, List
# Qt5 imports.
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR, QSize
from PyQt5.QtWidgets import QSplitter, QMainWindow, QWidget, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QSizePolicy


class WeatherWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(WeatherWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        


def test_weather_widget():
    pass


if __name__ == '__main__':
    test_weather_widget()