#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import *
from pathlib import Path
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.titlebar import TitleBar, WindowTitleBar
# PyQt5 imports
# from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtGui import QFontDatabase, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QWidget, QMainWindow, QTabWidget, QLabel, QToolButton, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QScrollArea


class DashWidgetGroupBtnStyler:
    def __init__(self):
        self.templates = {}

    def __call__(self, style, **options):
        return self.templates[style]

class DashWidgetGroupStyler:
    pass

DASH_WIDGET_GROUP_BTN_STYLESHEET = jinja2.Template("""
QToolButton {
    color: #fff;
    border: 0px;
    font-size: 14px;
    background: transparent;
}
QToolButton:hover {
    color: #292929;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #eb5f34, stop: 0.9 #338fc0);
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}""")
DASH_WIDGET_GROUP = jinja2.Template("""
""")
def styleContextMenu(menu, accent_color: str="yellow"):
    menu.setAttribute(Qt.WA_TranslucentBackground)
    menu.setObjectName("FigDMenu")
    menu.setStyleSheet(jinja2.Template("""
    QMenu#FigDMenu {
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
    	color: #fff;
    	padding: 10px;
    	border-radius: 15px;
    }
    QMenu#FigDMenu::item:selected {
    	color: #fff; 
        border-radius: 5px;
    	background-color: {{ ACCENT_COLOR }}; 
    }
    QMenu#FigDMenu:separator {
    	background: #292929;
    }""").render(ACCENT_COLOR=accent_color))
    palette = menu.palette()
    palette.setColor(QPalette.Base, QColor(48,48,48))
    palette.setColor(QPalette.Text, QColor(125,125,125))
    palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    # palette.setColor(QPalette.PlaceholderText, QColor(125,125,125))
    palette.setColor(QPalette.Window, QColor(255,255,255))
    palette.setColor(QPalette.Highlight, QColor(235,95,52))
    menu.setPalette(palette)

    return menu

class DashWidgetGroupBtn(QToolButton):
    '''Dash Widget button'''
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashWidgetGroupBtn, self).__init__(parent)
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        icon = args.get("icon")
        text = args.get("text")
        style = args.get("style")
        self.hover_response = "background"
        if icon:
            self.inactive_icon = args["icon"]
            stem, ext = os.path.splitext(Path(args["icon"]))
            self.active_icon = f"{stem}_active{ext}"
            if os.path.exists(FigD.icon(self.active_icon)):
                self.hover_response = "foreground"
            self.setIcon(FigD.Icon(self.inactive_icon))
        if text: self.setText(args["text"])
        if style: self.setToolButtonStyle(style)
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStatusTip(tip)
        # stylesheet attributes.
        background = args.get("background", "transparent")
        # print(font_size)
        if self.hover_response == "background":
            self.setStyleSheet(jinja2.Template('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: {{ background }};
            }
            QToolButton:hover {
                color: #292929;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220));
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''').render(
                    background=background,
                )
            )
        else:
            self.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: transparent;
            }
            QToolButton:hover {
                color: #eb5f34;
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''')

    def leaveEvent(self, event):
        if self.hover_response == "foreground":
            self.setIcon(FigD.Icon(self.inactive_icon))
        super(DashWidgetGroupBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        if self.hover_response == "foreground":
            self.setIcon(FigD.Icon(self.active_icon))
        super(DashWidgetGroupBtn, self).enterEvent(event)


class DashWidgetGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: str="Widget Group"):
        super(DashWidgetGroup, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.group = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(2)
        self.group.setLayout(self.layout)
        self.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
            margin-left: 5px;
            margin-right: 5px;
        }""")
        layout.addStretch(1)
        layout.addWidget(self.group)
        layout.addWidget(self.Label(name))
        self.setLayout(layout)

    def addWidget(self, *args, **kwargs):
        self.layout.addWidget(*args, **kwargs)

    def Label(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #6e6e6e; /* #eb5f34; */
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }''')
        return name

    def initBtnGroup(self, btn_args, orient="horizontal", 
                     alignment_flag=None, spacing=None):
        btnGroup = QWidget()
        btnGroup.btns = []
        if orient == "horizontal":
            layout = QHBoxLayout()
        elif orient == "vertical":
            layout = QVBoxLayout()
        if spacing is not None:
            # print("setting spacing")
            layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)
        btnGroup.layout = layout
        btnGroup.setLayout(layout)
        btnGroup.setStyleSheet('''
        QWidget {
            color: #fff;
            border: 0px;
            font-size: 10px;
            background: transparent;
        }''')
        layout.addStretch(1)
        for args in btn_args:
            btn = self.initBtn(**args)
            btnGroup.btns.append(btn)
            if alignment_flag is None:
                layout.addWidget(btn, 0, Qt.AlignCenter)
            else:
                layout.addWidget(btn, 0, alignment_flag)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def initBtn(self, **args):
        return DashWidgetGroupBtn(self, **args)


class FigDAppContainer(QApplication):
    def __init__(self, *args, **kwargs):
        super(FigDAppContainer, self).__init__(*args, **kwargs)
        self.active_window_ptr = None
        # tray_icon = args.get("icon", "lol")
        # create tray menu.
        self.trayMenu = self.initTrayMenu()

    def createTrayIcon(self, tray_icon: str):
        # tray icon button.
        self.trayIcon = QSystemTrayIcon(FigD.Icon(tray_icon), self)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

    def initTrayMenu(self) -> QMenu:
        """create context menu for system tray icon.

        Returns:
            QMenu: context menu object.
        """
        # actions for tray icon context menu.
        self.showAction = QAction("Open")
        self.quitAction = QAction("Quit")
        self.logsAction = QAction("Get logs")
        self.supportAction = QAction("Collect support files")
        self.settingsAction = QAction("Settings")
        # add icons.
        self.showAction.setIcon(FigD.Icon("tray/open.svg"))
        self.quitAction.setIcon(FigD.Icon("tray/close.svg"))
        self.logsAction.setIcon(FigD.Icon("tray/logs.svg"))
        self.supportAction.setIcon(FigD.Icon("tray/logs.svg"))
        self.settingsAction.setIcon(FigD.Icon("tray/settings.svg"))
        # connect functions to actions.
        self.showAction.triggered.connect(self.showActiveWindow)
        self.quitAction.triggered.connect(self.quit)
        # tray icon menu.
        trayMenu = QMenu()
        trayMenu.addAction(self.logsAction)
        trayMenu.addAction(self.supportAction)
        trayMenu.addSeparator()
        trayMenu.addAction(self.settingsAction)
        trayMenu.addSeparator()
        trayMenu.addAction(self.showAction)
        trayMenu.addAction(self.quitAction)

        return trayMenu

    def showActiveWindow(self):
        window = QApplication.activeWindow()
        window.show()

    def notify(self, obj, event):
        if isinstance(obj, FigDWindow):
            if event.type() == QEvent.WindowDeactivate:
                # print("deactivated", obj.appName)
                obj.titlebar.deactivate()
            if event.type() == QEvent.WindowActivate:
                # print("activated", obj.appName)
                obj.titlebar.activate()

        return super(FigDAppContainer, self).notify(obj, event)


class FigDTabWidget(QTabWidget):
    def __init__(self):
        super(FigDTabWidget, self).__init__()
        self.setStyleSheet("""
        QTabWidget {
            color: #fff;
            border: 0px;
            font-family: 'Be Vietnam Pro';
            background: transparent;
        }
        QTabWidget::pane {
            border: 0px;
            background: transparent;
        }
        QTabBar {
            border: 0px;
            background: transparent;
        }
        QTabBar::close-button {
            background: url("/home/atharva/GUI/fig-dash/resources/icons/close.png");
            background-repeat: no-repeat;
            background-position: center;
        }
        QTabBar::close-button:hover {
            background: url("/home/atharva/GUI/fig-dash/resources/icons/close-active.png");
            background-repeat: no-repeat;
            background-position: center;
        }
        QTabBar::tab {
            border: 0px;
            color: #fff;

            margin-left: 1px;
            margin-right: 1px;

            padding-top: 5px;
            padding-left: 9px;
            padding-right: 5px;
            padding-bottom: 5px;

            font-size: 17px;
            font-family: 'Be Vietnam Pro', sans-serif;
            max-width: 300px;
            background: #000;
        }
        QTabBar::tab:hover {
            color: #fff;
            background: #323232;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 200), stop : 0.3 rgba(191, 54, 54, 220), stop : 0.6 rgba(235, 95, 52, 220), stop: 0.9 rgba(235, 204, 52, 220)); */
        }
        QTabBar::tab:selected {
            color: #eee;
            border: 0px;
            background: #323232;
            font-weight: bold;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e4852c, stop : 0.143 #e4822d, stop : 0.286 #e4802f, stop : 0.429 #e47d30, stop : 0.571 #e47b32, stop : 0.714 #e47833, stop : 0.857 #e47635, stop : 1.0 #e47336); */
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
            padding-top: 5px;
            padding-left: 9px;
            padding-right: 5px;
            padding-bottom: 5px;
            margin-left: 1px;
            margin-right: 1px;
            font-size: 17px;
            font-weight: bold;
        }""")
        self.setTabBarAutoHide(True)
        self.setAttribute(Qt.WA_TranslucentBackground)


class FigDWindow(QMainWindow):
    def __init__(self, widget, **args):
        # self.layout.insertWidget(0, titlebar)
        # set window icon, title and flags.
        super(FigDWindow, self).__init__()
        title = args.get("title", "FigD wrapped widget")
        winIcon = args.get("icon", "system/clipboard/window_icon.png")
        self.__win_icon_size = args.get("size", (30,30))
        self.setWindowTitle(title)
        self.setWindowIcon(FigD.Icon(winIcon))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setCentralWidget(widget)
        self.installEventFilter(self)
        self.titlebar = None
        self.shortcuts_pane = self.createShortcutsPane()

    def printShortcuts(self):
        for action in self.findChildren(QAction):
            print(type(action), action.text(), action.toolTip(), [x.toString() for x in action.shortcuts()])

    def createShortcutLine(self, shortcut: str, action: str) -> QWidget:
        line = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        line.setLayout(layout)
        line.setStyleSheet("background: transparent;") 
        keys = shortcut.split("+")
        for key in keys[:-1]:
            keyBtn = QToolButton()
            keyBtn.setStyleSheet("""
            QToolButton {
                color: #aaa;
                padding-top: 4px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 4px;
                font-size: 16px;
                border-radius: 6px;
                background: #484848;
            }""")
            keyBtn.setText(key)
            layout.addWidget(keyBtn, 0, Qt.AlignLeft | Qt.AlignVCenter)
            # add plus as a label
            plus = QLabel()
            plus.setStyleSheet("""
            QLabel {
                color: #aaa;
                background: transparent;
            }""")
            plus.setText("+")
            layout.addWidget(plus, 0, Qt.AlignLeft | Qt.AlignVCenter)
        keyBtn = QToolButton()
        keyBtn.setStyleSheet("""
        QToolButton {
            color: #aaa;
            padding-top: 4px;
            padding-left: 8px;
            padding-right: 8px;
            padding-bottom: 4px;
            font-size: 16px;
            border-radius: 6px;
            background: #484848;
        }""")
        keyBtn.setText(keys[-1])
        layout.addWidget(keyBtn, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout.addStretch(1)
        # add description text for the action.
        description = QLabel()
        description.setStyleSheet("""
        QLabel {
            color: #fff;
            font-size: 16px;
            font-family: 'Be Vietnam Pro';
            background: transparent;
        }""")
        description.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        description.setText(action)
        layout.addWidget(description)

        return line

    def createShortcutsPane(self) -> QMainWindow:
        window = QMainWindow()
        window.setAttribute(Qt.WA_TranslucentBackground)
        window.setWindowFlags(Qt.Popup)
        shortcuts_widget = QScrollArea()
        shortcuts_widget.setStyleSheet("""
        QWidget {
            border-radius: 20px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        }""")
        shortcuts_list = QWidget()
        shortcuts_list.setStyleSheet("""
        color: #eee;
        background: transparent;""")
        vboxlayout = QVBoxLayout()
        shortcuts_list.setLayout(vboxlayout)
        for action in self.findChildren(QAction):
            shortcuts = [shortcut.toString() for shortcut in action.shortcuts()]
            if len(shortcuts) == 0: continue
            for shortcut in shortcuts:
                print(shortcut)
                vboxlayout.addWidget(
                    self.createShortcutLine(
                        shortcut,
                        action.text(),
                    )
                )
        shortcuts_widget.setWidget(shortcuts_list)
        window.setCentralWidget(shortcuts_widget)

        return window
    # def focusInEvent(self, event):
    #     if self.titlebar: self.titlebar.activate()
    #     super(FigDWindow, self).focusInEvent(event)
    # def focusOutEvent(self, event):
    #     if self.titlebar: self.titlebar.deactivate()
    #     super(FigDWindow, self).focusOutEvent(event)
        # self.setStyleSheet("""
        # QMainWindow {
        #     border-radius: 20px;
        #     background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        # }""")
    def showShortcutList(self):
        self.shortcuts_pane.show()
    
    def connectTitleBar(self, titlebar):
        self.titlebar = titlebar
        self.titlebar.setWindowIcon(
            self.windowIcon(), 
            size=self.__win_icon_size,
        )
        self.titlebar.connectWindow(self)

    def define(self, *args, **kwargs):
        if self.titlebar:
            self.titlebar.define(*args, **kwargs)

def extract_colors_from_qt_grad(qt_grad: str) -> List[str]:
    return ["#"+i.split("#")[-1] for i in ("#"+"#".join(qt_grad.split(")")[0].split("#")[1:])).split(",")]

def create_css_grad(colors: List[str], angle: int=90) -> str:
    """create css gradients from a list of hex colors, and angle (in integers).

    Returns:
        str: css gradient string.
    """
    css_grad = f"linear-gradient({angle}deg, "
    css_grad += ", ".join(colors)
    css_grad += ")"

    return css_grad

def wrapFigDWindow(widget: QWidget, **args):
    QFontDatabase.addApplicationFont(
        FigD.font("BeVietnamPro-Regular.ttf")
    )
    # arguments.
    icon = args.get("icon")
    name = args.get("name", "-")
    title = args.get("title", "")
    width = args.get("width", 960)
    height = args.get("height", 800)
    add_tabs = args.get("add_tabs", True)
    animated = args.get("animated", False)
    show_titlebar = args.get("titlebar", True)
    accent_color = args.get("accent_color", "red")
    titlebar_callbacks = args.get("titlebar_callbacks", {})
    # create the titlebar.
    titlebar = WindowTitleBar(
        background=accent_color, 
        callbacks=titlebar_callbacks,
        title_widget=args.get("title_widget"),
    )
    if animated: titlebar.setAnimatedTitle(title)
    else: titlebar.setTitle(title)
    try:
        titlebar.ribbonCollapseBtn.clicked.connect(widget.menu.toggle)
    except Exception as e: print(e)
    if not show_titlebar: titlebar.hide()
    centralWidget = QWidget()
    centralWidget.setObjectName("FigDUI")
    centralWidget.setStyleSheet("""
    QWidget#FigDUI {
        border-radius: 20px;
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
    }
    QScrollBar:vertical {
        border: 0px solid #999999;
        width: 12px;
        margin: 0px 0px 0px 0px;
        background-color: rgba(255, 255, 255, 0);
    }
    QScrollBar:horizontal {
        border: 0px solid #999999;
        width: 12px;
        margin: 0px 0px 0px 0px;
        background-color: rgba(255, 255, 255, 0);
    }
    /* QScrollBar:vertical:hover {
        background-color: rgba(255, 253, 184, 0.3);
    } */
    QScrollBar::handle:vertical {
        min-height: 0px;
        border: 0px solid red;
        border-radius: 0px;
        /* background-color: transparent; */
        background-color: rgba(255, 255, 255, 0.2);
    }
    QScrollBar::handle:horizontal {
        min-width: 0px;
        border: 0px solid red;
        border-radius: 0px;
        /* background-color: transparent; */
        background-color: rgba(255, 255, 255, 0.2);
    }
    QScrollBar::handle:vertical:hover {
        background-color: rgba(255, 255, 255, 0.5);
    }
    QScrollBar::handle:horizontal:hover {
        background-color: rgba(255, 255, 255, 0.5);
    }
    QScrollBar::add-line:horizontal {
        width: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal {
        width: 0 px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:vertical {
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        height: 0 px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }""")
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    # build layout.
    layout.addWidget(titlebar)
    if add_tabs:
        tabwidget = FigDTabWidget()
        tabwidget.addTab(widget, name)
        layout.addWidget(tabwidget)
    else:
        layout.addWidget(widget)
    centralWidget.setLayout(layout)

    window = FigDWindow(widget=centralWidget, **args)
    window.appName = name
    window.connectTitleBar(titlebar)
    # style application tooltips
    app = QApplication.instance()
    if icon is not None:
        app.createTrayIcon(tray_icon=icon)
    app.setStyleSheet("""
    QToolTip {
        color: #fff;
        border: 0px;
        padding-top: -1px;
        padding-left: 5px;
        padding-right: 5px;
        padding-bottom: -1px;
        font-size:  17px;
        background: #000;
        font-family: 'Be Vietnam Pro', sans-serif;
    }""")
    # try: app.appendTitleBar(titlebar)
    # except Exception as e: print(e)
    # reposition window
    window.setGeometry(100, 100, width, height)
    screen_rect = app.desktop().screenGeometry()
    w, h = screen_rect.width()//2, screen_rect.height()//2
    widget.window_ptr = window
    window.move(w, h)

    return window