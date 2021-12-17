#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Union
# Qt imports.
# from PyQt5.QtGui import 
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QFileIconProvider
# fig-dash imports.
from ..utils import collapseuser


class TabsDropdown(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabsDropdown, self).__init__(parent)
        self.setObjectName("TabsDropdown")


class DashTabWidget(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(DashTabWidget, self).__init__(parent)
        self.dropdownBtn = TabsDropdown(self)
        self.icon_provider = QFileIconProvider()
        self.setTabsClosable(True)
        self.setElideMode(True)
        self.setMovable(True)
        self.setCornerWidget(self.dropdownBtn)
        self.setObjectName("DashTabWidget")

    def openFile(self, path: str):
        icon = self.getIcon(path)
        label = QLabel()
        label.setText(open(path).read())
        title = collapseuser(path)
        self.addTab(label, icon, title)

    def getIcon(self, path: str):
        file_info = QFileInfo(path)
        return self.icon_provider.icon(file_info)