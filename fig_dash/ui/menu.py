#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout


class DashMenu(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(DashMenu, self).__init__(parent)
        self.filemenu = self.initFilemenu()
        self.addTab(self.filemenu, "file")        
        self.collapse()

    @property
    def collapsed(self):
        return self._collapsed

    @collapsed.setter
    def collapsed(self, value):
        pass

    def expand(self):
        width = self.width()
        self._collapsed = False
        self.resize(width, 100)

    def collapse(self):
        self._collapsed = True
        self.setMaximumHeight(30)

    def toggle(self):
        if self.collapsed:
            self.expand()
        else:
            self.collapse()

    def initFileMenu(self):
        filemenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel("File Menu"))
        filemenu.setLayout(layout)

        return filemenu
