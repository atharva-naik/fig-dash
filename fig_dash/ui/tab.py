#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Union
# Qt imports.
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton


class TabsDropdown(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabsDropdown, self).__init__(parent)


class DashTabWidget(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(DashTabWidget, self).__init__(parent)
        self.dropdownBtn = TabsDropdown(self)
        self.setCornerWidget(self.dropdownBtn)
    