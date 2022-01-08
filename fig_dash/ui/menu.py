#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QFrame, QAction, QVBoxLayout, QHBoxLayout
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.widget.git import DashGitUI
from fig_dash.ui.widget.jupyter_nb import JupyterNBWidget
from fig_dash.ui.widget.codemirror import CodeMirrorEditor
from fig_dash.ui.system.fileviewer import FileViewerWidget


menu_style = '''
QWidget#DashMenuTab {
    border: 0px;
    background: transparent;
}
QWidget#DashSubMenu {
    /* border: 1px solid #eb5f34; */
    background: transparent;
}
QTabWidget {
    color: #fff;
    border: 0px;
    background: transparent;
}
QTabWidget::pane {
    border: 0px;
    background: transparent;
}
QTabBar {
    background: transparent;
    border: 0px;
    padding: 2px;
    border: 0px;
}
QTabBar::tab {
    border: 0px;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 5px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 3px;
    margin-bottom: 3px;
    border-bottom: 2px solid transparent;
    /* border-bottom: 4px solid #bf3636; */
}
QTabBar::tab:hover {
    color: #bf3636;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop : 0.6 #eb5f34, stop: 0.9 #ebcc34); */
}
QTabBar::tab:selected {
    border: 0px;
    color: #eb5f34;
    font-size: 18px;
    font-weight: bold;
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 5px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 3px;
    margin-bottom: 3px;
    border-bottom: 2px solid #eb5f34;
    /* border-bottom: 4px solid #bf3636; */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
}'''
class DashMenu(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashMenu, self).__init__(parent)
        self.toggleBtn = self.initToggleBtn()
        self.filemenu = self.initFileMenu(**args)
        self.editmenu = self.initEditMenu(**args)
        self.codemenu = self.initCodeMenu(**args)
        self.addTab(self.filemenu, "File")        
        self.addTab(self.editmenu, "Edit")
        self.addTab(self.codemenu, "Code")        
        self.collapse()
        # self.currentChanged.connect(self.onTabChange)
        self.tabBarClicked.connect(self.tabToggle)
        self.setStyleSheet(menu_style)
        self.setCornerWidget(self.toggleBtn)

    def tabToggle(self, i):
        '''check if currently active tab is clicked. If so toggle visibility of menubar.'''
        # print(self.currentIndex(), i)
        if i == self.currentIndex(): 
            self.toggle()
        else: self.expand()

    def initToggleBtn(self):
        btn = QToolButton()
        btn.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')
        btn.clicked.connect(self.toggle)

        return btn

    def onTabChange(self, i: int):
        self.expand()

    @property
    def collapsed(self):
        return self._collapsed

    @collapsed.setter
    def collapsed(self, value):
        pass

    def expand(self):
        self._collapsed = False
        self.toggleBtn.setIcon(FigD.Icon("menu/collapse.svg"))
        self.setFixedHeight(160)

    def collapse(self):
        self._collapsed = True
        self.toggleBtn.setIcon(FigD.Icon("menu/expand.svg"))
        self.setFixedHeight(35)

    def toggle(self):
        # print(self.collapsed)
        if self.collapsed:
            self.expand()
        else:
            self.collapse()

    def initFileMenu(self, **args):
        filemenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.fileviewer = FileViewerWidget(
            background=args.get("wallpaper")
        )
        layout.addWidget(self.fileviewer.menu)
        filemenu.setLayout(layout)
        filemenu.setObjectName("DashMenuTab")

        return filemenu

    def initBrowserMenu(self, **args):
        browsermenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel("File Menu"))
        browsermenu.setLayout(layout)
        browsermenu.setObjectName("DashMenuTab")

    def initEditMenu(self, **args):
        editmenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel("Edit Menu"))
        editmenu.setLayout(layout)
        editmenu.setObjectName("DashMenuTab")

        return editmenu

    def menuName(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            padding: 6px;
            color: #eb5f34;
            font-size: 16px;
            background: transparent;
        }''')
        return name

    def initCodeMenu(self, **args):
        codemenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # create widgets.
        self.juputer_nb = JupyterNBWidget() # jupyter notebook.
        self.cm_editor = CodeMirrorEditor() # codemirror editor.
        self.git_ui = DashGitUI()
       
        CMToolbar = QWidget()
        # CMToolbar.setAttribute(Qt.WA_TranslucentBackground)
        CMToolbar.setObjectName("DashSubMenu")
        CMLayout = QVBoxLayout()
        CMLayout.setContentsMargins(0, 0, 0, 0)
        CMLayout.setSpacing(0)
        CMLayout.addWidget(self.menuName("Editor Tools"))
        CMLayout.addWidget(self.cm_editor.viewtoolbar)
        CMLayout.addWidget(self.cm_editor.codetoolbar)
        CMLayout.addStretch(1)
        CMToolbar.setLayout(CMLayout)

        VCSToolbar = QWidget()
        # VCSToolbar.setAttribute(Qt.WA_TranslucentBackground)
        VCSToolbar.setObjectName("DashSubMenu")
        VCSLayout = QVBoxLayout()
        VCSLayout.setContentsMargins(0, 0, 0, 0)
        VCSLayout.setSpacing(0)
        VCSLayout.addWidget(self.menuName("Version Control"))
        VCSLayout.addWidget(self.git_ui.repo_toolbar)
        VCSLayout.addWidget(self.git_ui.branch_toolbar)
        VCSLayout.addWidget(self.git_ui.edit_toolbar)
        VCSLayout.addStretch(1)
        VCSToolbar.setLayout(VCSLayout) 

        IPyToolbar = QWidget()
        # IPyToolbar.setAttribute(Qt.WA_TranslucentBackground)
        IPyToolbar.setObjectName("DashSubMenu")
        IPyLayout = QVBoxLayout()
        IPyLayout.setContentsMargins(0, 0, 0, 0)
        IPyLayout.setSpacing(0)
        IPyLayout.addWidget(self.menuName("IPython Tools"))
        IPyLayout.addWidget(self.juputer_nb.menubar, 0, Qt.AlignCenter)
        IPyLayout.addWidget(self.juputer_nb.cellbar, 0, Qt.AlignCenter)
        IPyLayout.addWidget(self.juputer_nb.kernelbar, 0, Qt.AlignCenter)
        IPyLayout.addStretch(1)
        IPyToolbar.setLayout(IPyLayout)
        # add all submenus.
        layout.addWidget(CMToolbar)
        layout.addWidget(self.addSeparator())
        layout.addWidget(VCSToolbar)
        layout.addWidget(self.addSeparator())
        layout.addWidget(IPyToolbar)
        layout.addStretch(1)
        codemenu.setLayout(layout)
        codemenu.setObjectName("DashMenuTab")

        return codemenu

    def addSeparator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet('''background: #292929''')
        sep.setLineWidth(1)
        sep.setMaximumHeight(90)

        return sep


def test_menu():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    dashmenu = DashMenu()
    dashmenu.setAttribute(Qt.WA_TranslucentBackground)
    dashmenu.setWindowFlags(Qt.WindowStaysOnTopHint)
    dashmenu.show()
    app.exec()


if __name__ == "__main__":
    test_menu()