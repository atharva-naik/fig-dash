#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from tkinter import Button
from fig_dash.ui.tab import DashTabWidget
import jinja2
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtCore import Qt, QSize, QObject, QPoint, QEvent
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QFrame, QAction, QVBoxLayout, QHBoxLayout
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.widget.git import DashGitUI
from fig_dash.ui.widget.jupyter_nb import JupyterNBWidget
from fig_dash.ui.widget.codemirror import CodeMirrorEditor
from fig_dash.ui.system.fileviewer import FileViewerWidget


menu_background = "transparent" 
menu_style = '''
QWidget#DashMenuTab {
    border: 0px;
    background: '''+menu_background+''';
}
QWidget#DashSubMenu {
    /* border: 1px solid #eb5f34; */
    background: '''+menu_background+''';
}
QTabWidget {
    color: #fff;
    border: 0px;
    background: '''+menu_background+''';
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
    font-size: 17px;
    font-weight: bold;
    font-family: 'Be Vietnam Pro', sans-serif;
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
    font-size: 17px;
    font-weight: bold;
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 5px;
    margin-top: 3px;
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: 3px;
    border-bottom: 2px solid #eb5f34;
    /* border-bottom: 4px solid #bf3636; */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
}'''
class BrowserStatusBar(QWidget):
    def __init__(self) -> None:
        super(BrowserStatusBar, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.selectedTextIndicator = self.initBtn(
            icon="select_text.png",
            text=" None"
        )
        self.scrollPosIndicator = self.initBtn(
            icon="scroll.png",
            text=" (0,0)",
        )
        self.layout.addWidget(self.selectedTextIndicator)
        self.layout.addWidget(self.scrollPosIndicator)
        self.setLayout(self.layout)

    def initBtn(self, icon: str=None, text: str=None) -> QToolButton:
        """[summary]

        Args:
            icon (str, optional): [description]. Defaults to None.
            text (str, optional): [description]. Defaults to None.

        Returns:
            QToolButton: [description]
        """
        btn = QToolButton(self)
        if icon: 
            icon = os.path.join("browser", icon)
            btn.setIcon(FigD.Icon(icon))
        if text: btn.setText(text)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setStyleSheet("background: #292929; color: #fff;")
        btn.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QToolButton:hover {
            border: 0px;
            background: rgba(0, 0, 0, 0.5);
        }''')

        return btn

    def updateScrollPos(self, x: float, y: float):
        self.scrollPosIndicator.setText(f"({x:.0f},{y:.0f})")

    def updateSelection(self, text: str):
        self.selectedTextIndicator.setText(" "+text)


class DashMenu(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashMenu, self).__init__(parent)
        self.toggleBtn = self.initToggleBtn()
        self.filemenu = self.initFileMenu(**args)
        self.editmenu = self.initEditMenu(**args)
        self.viewmenu = self.initViewMenu(**args)
        self.codemenu = self.initCodeMenu(**args)
        self.formatmenu = self.initFormatMenu(**args)
        self.browsermenu = self.initBrowserMenu(**args)
        self.addTab(self.filemenu, "File")        
        self.addTab(self.editmenu, "Edit")
        self.addTab(self.formatmenu, "Format")
        self.addTab(self.viewmenu, "View")
        self.addTab(self.codemenu, "Code")
        self.addTab(self.browsermenu, "Browser")     
        # self.currentChanged.connect(self.onTabChange)
        self.browser_statusbar = BrowserStatusBar()
        self.browser_statusbar.hide()
        self.tabBarClicked.connect(self.tabToggle)
        self.setStyleSheet(menu_style)
        self.setCornerWidget(self.toggleBtn)
        # set browser index.
        self.setCurrentIndex(6-1)
        self.collapse()

    def updateStatusBar(self, i: int):
        if i == 1-1:
            self.fileviewer.statusbar.show()
        else:
            self.fileviewer.statusbar.hide()
        if i == 5-1:
            self.cm_editor.statusbar.show()
        else:
            self.cm_editor.statusbar.hide()
        if i == 6-1:
            self.browser_statusbar.show()
        else:
            self.browser_statusbar.hide()

    def setCurrentIndex(self, i: int):
        self.updateStatusBar(i)
        super(DashMenu, self).setCurrentIndex(i)

    def tabToggle(self, i):
        '''check if currently active tab is clicked. If so toggle visibility of menubar.'''
        # print(self.currentIndex(), i)
        if i == self.currentIndex(): 
            self.toggle()
        else: self.expand()
        self.updateStatusBar(i)

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

    def initViewMenu(self, **args):
        viewmenu = QWidget()
        # layout = QHBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        # self.fileviewer = FileViewerWidget(
        #     background=args.get("wallpaper")
        # )
        # layout.addWidget(self.viewmenu)
        # viewmenu.setLayout(layout)
        viewmenu.setObjectName("DashMenuTab")

        return viewmenu

    def initFormatMenu(self, **args):
        formatmenu = QWidget()
        formatmenu.setObjectName("DashMenuTab")

        return formatmenu

    def initBrowserMenu(self, **args):
        browsermenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.devToolsBtn = QToolButton()
        layout.addWidget(self.devToolsBtn)
        browsermenu.setLayout(layout)
        browsermenu.setObjectName("DashMenuTab")

        return browsermenu

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
        self.cm_editor.statusbar.hide()
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
        sep.setStyleSheet(f'''background: #292929''')
        sep.setLineWidth(4)
        sep.setMaximumHeight(100)

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