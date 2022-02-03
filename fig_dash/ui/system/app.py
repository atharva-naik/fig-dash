#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy


class AppLauncher(QWidget):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(AppLauncher, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def init(self, folder):
        pass