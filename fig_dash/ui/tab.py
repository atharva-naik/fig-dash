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


class TabsSearchDropdown(QWidget):
    def __init__(self, btn):
        super(TabsSearchDropdown, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Popup)
        self.btn = btn
        layout = QVBoxLayout()
        
        self.setObjectName("TabsSearchDropdown")
        self.searchbar = self.initSearchBar()
        layout.addWidget(self.searchbar)
        layout.addWidget(QLabel("this is something"))
        self.setLayout(layout)
        self.setFixedWidth(300)

    def initPos(self, width: int, offset: int=200):
        geo = self.geometry()
        pos = self.btn.pos()
        w, h = geo.width(), geo.height()
        x, y = pos.x()+width-offset, pos.y()+h/2
        print(f"setGeometry({x}, {y}, {w}, {h})")
        self.setGeometry(x, y, w, h)

    def rePos(self, width: int, offset: int=200):
        geo = self.geometry()
        pos = self.btn.pos()
        w, h = geo.width(), geo.height()
        x, y = pos.x()-180, pos.y()+h/2
        # print(f"setGeometry({x}, {y}, {w}, {h})")
        self.setGeometry(x, y, w, h)

    def initSearchBar(self):
        searchbar = QLineEdit(self)
        searchAction = QAction()
        searchAction.setIcon(QIcon("/home/atharva/GUI/fig-dash/resources/icons/tabbar/search.svg"))
        searchbar.addAction(searchAction)

        return searchbar

    def Show(self):
        self.show()
    # def Move(self, x: int, y: int):
    #     self.setGeometry(x-100, y+100, 100, 100)
class TabsSearchBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabsSearchBtn, self).__init__(parent)
        self.setObjectName("TabsSearchBtn")
        self.dropdown = TabsSearchDropdown(btn=self)
        self.clicked.connect(self.dropdown.Show)
    #     contextMenu = self.initDropdown()
    #     contextMenu.exec_(self.mapToGlobal(event.pos()))        
    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     quitAct = contextMenu.addAction("Close Search")
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         self.close()
class DashTabWidget(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(DashTabWidget, self).__init__(parent)
        self.dropdownBtn = TabsSearchBtn(self)
        self.dropdown = self.dropdownBtn.dropdown
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