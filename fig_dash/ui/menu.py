#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtCore import Qt, QSize, QObject, QPoint, QEvent
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QFrame, QAction, QVBoxLayout, QHBoxLayout, QScrollArea
# fig-dash imports.
from fig_dash.ui import DashWidgetGroup
from fig_dash.assets import FigD
from fig_dash.ui.browser import BrowserMenu
from fig_dash.ui.widget.git import DashGitUI
from fig_dash.ui.widget.jupyter_nb import JupyterNBWidget
from fig_dash.ui.widget.codemirror import CodeMirrorEditor
from fig_dash.ui.system.fileviewer import FileViewerWidget


menu_background = "#000" 
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
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e45c33, stop : 0.143 #e46231, stop : 0.286 #e56830, stop : 0.429 #e56e2e, stop : 0.571 #e5742d, stop : 0.714 #e57a2d, stop : 0.857 #e47f2c, stop : 1.0 #e4852c);
    border: 0px;
    padding: 2px;
    border: 0px;
}
QTabBar::tab {
    border: 0px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;

    color: #fff;
    background: transparent;

    font-size: 17px;
    font-weight: bold;
    font-family: 'Be Vietnam Pro', sans-serif;
    
    padding-top: 4px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 4px;
    
    margin-left: 0px;
    margin-right: 0px;
    margin-top: 0px;
    margin-bottom: 0px;
    /* border-bottom: 2px solid transparent;
       border-bottom: 4px solid #bf3636; */
}
QTabBar::tab:hover {
    color: #292929;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop : 0.6 #eb5f34, stop: 0.9 #ebcc34); */
}
QTabBar::tab:selected {
    border: 0px;
    color: #eb5f34;
    font-size: 17px;
    font-weight: bold;
    
    padding-top: 4px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 4px;
    
    margin-left: 0px;
    margin-right: 0px;
    margin-top: 0px;
    margin-bottom: 0px;

    background: #000;
    /* border-bottom: 2px solid #ff9e28;
       border-bottom: 4px solid #bf3636;
       background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
}'''
menu_icon_set = [
    {
        "inactive": FigD.Icon(f"menu/{name}.svg"), 
        "active": FigD.Icon(f"menu/{name}_active.svg")
    } for name in [
        "file", "edit", "insert", "format",
        "view", "code", "browser", "mail",
        "music", "image", "video", "form",
        "event", "terminal", "device", 
        "create", "payment", "entertainment",
    ]
]
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


class ViewMenuVisGroup(DashWidgetGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(ViewMenuVisGroup, self).__init__(parent, "Visibility")
        # widgets with togglable visibility.
        self.toggleGroup1 = self.initBtnGroup([
            {"icon": "browser/word_count.svg", "tip": "toggle visibility of word count, time to read display"},
            {"icon": "menu/tabs.png", "tip": "toggle visibility of tab bar"},
            {"icon": "menu/dock.svg", "tip": "toggle visibility of dock"},
        ], orient="vertical", spacing=5)
        self.toggleGroup2 = self.initBtnGroup([
            {"icon": "menu/sysutils.svg", "tip": "open system utilites menu"},
            {"icon": "menu/notifications.svg", "tip": "toggle visibility of notifications overlay"},
        ], orient="vertical", spacing=5)
        self.wordCountBtn = self.toggleGroup1.btns[0]
        self.tabToggleBtn = self.toggleGroup1.btns[1]
        self.dockBtn = self.toggleGroup1.btns[2]
        self.sysUtilsBtn = self.toggleGroup2.btns[0]
        self.notifsBtn = self.toggleGroup2.btns[1]
        # add widgets to layout.
        self.layout.addWidget(self.toggleGroup1, 0, Qt.AlignBottom)
        self.layout.addWidget(self.toggleGroup2, 0, Qt.AlignBottom)

    def connectWindow(self, window):
        self.dash_window = window
        # self.tabs = self.dash_window.tabs
        self.wordCountBtn.clicked.connect(
            window.page_info.toggle
        )
        titlebar = window.titlebar
        self.dockBtn.clicked.connect(
            titlebar.toggleInfo
        )
        self.tabToggleBtn.clicked.connect(
            window.tabs.toggleTabBar
        )
        self.sysUtilsBtn.clicked.connect(
            window.sysutilsbar.toggle
        )
        self.notifsBtn.clicked.connect(
            window.notifsPanel.toggle
        )


class ViewMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(ViewMenu, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # create groups.
        self.viewgroup = ViewMenuVisGroup()
        self.notifsBtn = self.viewgroup.notifsBtn
        # create layout.
        self.layout.addWidget(self.viewgroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addStretch(1)
        # set layout.
        self.setLayout(self.layout)

    def addSeparator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #292929''')
        sep.setLineWidth(2)
        sep.setMaximumHeight(100)

        return sep

    def connectWindow(self, widget):
        self.viewgroup.connectWindow(widget)


class DashMenu(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashMenu, self).__init__(parent)
        # self.setUsesScrollButtons(False)
        self.toggleBtn = self.initToggleBtn()
        
        self.filemenu = self.initFileMenu(**args)
        self.formmenu = self.initFormMenu(**args)
        self.editmenu = self.initEditMenu(**args)
        self.viewmenu = self.initViewMenu(**args)
        self.codemenu = self.initCodeMenu(**args)
        self.mailmenu = self.initMailMenu(**args)
        self.eventmenu = self.initEventMenu(**args)
        self.imagemenu = self.initImageMenu(**args)
        self.videomenu = self.initVideoMenu(**args)
        self.musicmenu = self.initMusicMenu(**args)
        self.insertmenu = self.initInsertMenu(**args)
        self.devicemenu = self.initDeviceMenu(**args)
        self.formatmenu = self.initFormatMenu(**args)
        self.browsermenu = self.initBrowserMenu(**args)
        self.terminalmenu = self.initTerminalMenu(**args)
        # create, payment, entertainment.
        self.createmenu = self.initCreateMenu(**args)
        self.paymentmenu = self.initPaymentMenu(**args)
        self.entertainmentmenu = self.initEntertainmentMenu(**args)

        self.addTab(self.filemenu, FigD.Icon("menu/file.svg"), "File")        
        self.addTab(self.editmenu, FigD.Icon("menu/edit.svg"), "Edit")
        self.addTab(self.insertmenu, FigD.Icon("menu/insert.svg"), "Insert")
        self.addTab(self.formatmenu, FigD.Icon("menu/format.svg"), "Format")
        self.addTab(self.viewmenu, FigD.Icon("menu/view.svg"), "View")
        self.addTab(self.codemenu, FigD.Icon("menu/code.svg"), "Code") 
        self.addTab(self.browsermenu, FigD.Icon("menu/browser.svg"), "Browser") 
        self.addTab(self.mailmenu, FigD.Icon("menu/mail.svg"), "Mail")    
        self.addTab(self.musicmenu, FigD.Icon("menu/music.svg"), "Music")
        self.addTab(self.imagemenu, FigD.Icon("menu/image.svg"), "Images")
        self.addTab(self.videomenu, FigD.Icon("menu/video.svg"), "Videos")
        self.addTab(self.formmenu, FigD.Icon("menu/form.svg"), "Forms")
        self.addTab(self.eventmenu, FigD.Icon("menu/event.svg"), "Events")
        self.addTab(self.terminalmenu, FigD.Icon("menu/terminal.svg"), "Terminal")
        self.addTab(self.devicemenu, FigD.Icon("menu/device.svg"), "Devices")
        self.addTab(self.createmenu, FigD.Icon("menu/create.svg"), "Create")
        self.addTab(self.paymentmenu, FigD.Icon("menu/payment.svg"), "Payments")
        self.addTab(self.entertainmentmenu, FigD.Icon("menu/entertainment.svg"), "Entertainment")
        self.currentChanged.connect(self.onTabChange)
        self.browser_statusbar = BrowserStatusBar()
        self.browser_statusbar.hide()
        self.tabBarClicked.connect(self.tabToggle)
        self.setStyleSheet(menu_style)
        self.setCornerWidget(self.toggleBtn)
        # set browser index.
        self.setCurrentIndex(7-1)
        self.collapse()

    def updateStatusBar(self, i: int):
        if i == 1-1:
            self.fileviewer.statusbar.show()
        else:
            self.fileviewer.statusbar.hide()
        if i == 6-1:
            self.cm_editor.statusbar.show()
        else:
            self.cm_editor.statusbar.hide()
        if i == 7-1:
            self.browser_statusbar.show()
        else:
            self.browser_statusbar.hide()

    def onTabChange(self, i: int):
        print(i)

    def setCurrentIndex(self, i: int):
        # i = self.currentIndex()
        # print(f"i: {i}")
        j = self.currentIndex()
        # print(menu_icon_set[j]["inactive"])
        # print(menu_icon_set[i]["active"])
        self.setTabIcon(j, menu_icon_set[j]["inactive"])
        self.setTabIcon(i, menu_icon_set[i]["active"])
        self.updateStatusBar(i)
        super(DashMenu, self).setCurrentIndex(i)

    def wrapInScrollArea(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setAttribute(Qt.WA_TranslucentBackground)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("""
        QScrollArea {
            border: 0px;
            background: """+menu_background+""";
        }""")

        return scrollArea

    def tabToggle(self, i):
        '''check if currently active tab is clicked. If so toggle visibility of menubar.'''
        # print(self.currentIndex(), i)
        j = self.currentIndex()
        self.setTabIcon(j, menu_icon_set[j]["inactive"])
        self.setTabIcon(i, menu_icon_set[i]["active"])
        if i == j: 
            self.toggle()
        else: 
            self.expand()
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
        self.setFixedHeight(165)

    def collapse(self):
        self._collapsed = True
        self.toggleBtn.setIcon(FigD.Icon("menu/expand.svg"))
        self.setFixedHeight(28)

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

        return self.wrapInScrollArea(filemenu)

    def initViewMenu(self, **args):
        self._viewmenu = ViewMenu()
        self._viewmenu.setObjectName("DashMenuTab")

        return self._viewmenu

    def initFormatMenu(self, **args):
        formatmenu = QWidget()
        formatmenu.setObjectName("DashMenuTab")

        return formatmenu

    def initTerminalMenu(self, **args):
        terminalmenu = QWidget()
        terminalmenu.setObjectName("DashMenuTab")

        return terminalmenu

    def initDeviceMenu(self, **args):
        """_summary_
        keep a track of/connect to mounted devices, VPN, peripherals, remote access to resources/servers, connect to mobile phone, bluetooth connections, casting etc.

        Returns:
            _type_: _description_
        """
        devicemenu = QWidget()
        devicemenu.setObjectName("DashMenuTab")

        return devicemenu

    def initCreateMenu(self, **args):
        createmenu = QWidget()
        createmenu.setObjectName("DashMenuTab")

        return createmenu

    def initPaymentMenu(self, **args):
        # paypal, credit card, ycrpto.
        paymentmenu = QWidget()
        paymentmenu.setObjectName("DashMenuTab")

        return paymentmenu

    def initEntertainmentMenu(self, **args):
        entertainmentmenu = QWidget()
        entertainmentmenu.setObjectName("DashMenuTab")

        return entertainmentmenu

    def initInsertMenu(self, **args):
        insertmenu = QWidget()
        insertmenu.setObjectName("DashMenuTab")

        return insertmenu

    def initMailMenu(self, **args):
        mailmenu = QWidget()
        mailmenu.setObjectName("DashMenuTab")

        return mailmenu

    def initImageMenu(self, **args):
        imagemenu = QWidget()
        imagemenu.setObjectName("DashMenuTab")

        return imagemenu

    def initVideoMenu(self, **args):
        videomenu = QWidget()
        videomenu.setObjectName("DashMenuTab")

        return videomenu

    def initMusicMenu(self, **args):
        musicmenu = QWidget()
        musicmenu.setObjectName("DashMenuTab")

        return musicmenu

    def initFormMenu(self, **args):
        """_summary_
        Create forms, polls, surveys and charts 

        Returns:
            _type_: _description_
        """
        formmenu = QWidget()
        formmenu.setObjectName("DashMenuTab")

        return formmenu

    def initBrowserMenu(self, **args):
        # web archive, shields, cookie management, ad block, content policy, reading list, bookmarks, password manager, history tools, permissions.
        browsermenu = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._browsermenu = BrowserMenu()
        layout.addWidget(self._browsermenu)
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

    def initEventMenu(self, **args):
        """_summary_
        schedule meetings (google, cisco, zoom) and manage calendar events, alarm, reminders.

        Returns:
            _type_: _description_
        """
        eventmenu = QWidget()
        eventmenu.setObjectName("DashMenuTab")

        return eventmenu        

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

    def connectWindow(self, window):
        self.dash_window = window
        self._browsermenu.connectWindow(window)
        self._viewmenu.connectWindow(window)

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