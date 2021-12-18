#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo, Qt, QPoint
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QFileIconProvider, QLineEdit, QMenu, QAction, QVBoxLayout
# fig-dash imports.
from ..utils import collapseuser


class TabsDropdown(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabsDropdown, self).__init__(parent)
        self.setObjectName("TabsDropdown")
        self.dropdown = self.initDropdown()
        self.dropdown.mapFromParent(QPoint(1, 0))
        self.dropdown.show()
        # self.clicked.connect(self.dropdown.show)
    # def mousePressEvent(self, event):
    #     self.dropdown = self.initDropdown()
    #     self.dropdown.setContextMenuPolicy(Qt.CustomContextMenu)
    #     contextMenu = self.initDropdown()
    #     contextMenu.exec_(self.mapToGlobal(event.pos()))        
        # super(TabsDropdown, self).mousePressEvent(event)
    def initDropdown(self):
        dropdown = QWidget(self)
        layout = QVBoxLayout()
        dropdown.setLayout(layout)
        dropdown.setObjectName("TabsDropdownMenu")
        searchbar = self.initSearchBar()
        layout.addWidget(searchbar)
        layout.addWidget(QLabel("this is something"))

        return dropdown

    def initSearchBar(self):
        searchbar = QLineEdit()
        searchAction = QAction()
        searchAction.setIcon(QIcon("/home/atharva/GUI/fig-dash/resources/icons/tabbar/search.svg"))
        searchbar.addAction(searchAction)

        return searchbar
    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     quitAct = contextMenu.addAction("Close Search")
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         self.close()
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