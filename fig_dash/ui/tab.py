#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo, Qt, QPoint, QMimeDatabase
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QFileIconProvider, QLineEdit, QMenu, QAction, QVBoxLayout
# fig-dash imports.
from ..utils import collapseuser
from fig_dash.assets import FigD


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
tab_search_btn_style = jinja2.Template('''
QToolButton {
    border: 0px;
    border-radius: 15px;
}
QToolButton:hover {
    background: rgba(125, 125, 125, 0.7);
}''')
class TabsSearchBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabsSearchBtn, self).__init__(parent)
        self.setObjectName("TabsSearchBtn")
        self.dropdown = TabsSearchDropdown(btn=self)
        self.clicked.connect(self.dropdown.Show)
        self.setIcon(FigD.Icon("tabbar/dropdown.svg"))
        self.setStyleSheet(tab_search_btn_style.render())
    #     contextMenu = self.initDropdown()
    #     contextMenu.exec_(self.mapToGlobal(event.pos()))        
    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     quitAct = contextMenu.addAction("Close Search")
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         self.close()
dash_tab_widget_style = jinja2.Template('''
QTabWidget {
    background: #292929;
}
QTabWidget::pane {
    border: 0px;
}''')
class DashTabWidget(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]):
        self.mimetype_db = QMimeDatabase()
        super(DashTabWidget, self).__init__(parent)
        self.dropdownBtn = TabsSearchBtn(self)
        self.dropdown = self.dropdownBtn.dropdown
        self.icon_provider = QFileIconProvider()
        self.setTabsClosable(True)
        self.setElideMode(True)
        self.setMovable(True)
        self.setCornerWidget(self.dropdownBtn)
        self.setObjectName("DashTabWidget")
        # print(dash_tab_widget_style.render())
        self.setStyleSheet(dash_tab_widget_style.render())
        self.tabIcons = []

    def openFile(self, path: str):
        iconName = self.getIconName(path)
        icon = QIcon.fromTheme(iconName)
        self.tabIcons.append(icon)
        # print(icon, iconName)
        label = QLabel()
        label.setText(open(path).read())
        title = collapseuser(path)
        self.addTab(label, self.tabIcons[-1], title)

    def getIconName(self, path: str):
        file_info = QFileInfo(path)
        mimeType = self.mimetype_db.mimeTypeForFile(file_info)
        # print(QIcon.fromTheme(mimeType.iconName()))
        iconName = mimeType.iconName() 
        # print(iconName, QIcon.fromTheme(iconName))
        return iconName