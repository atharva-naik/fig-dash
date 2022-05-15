#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-

# combined app launcher and store.

import os
from typing import *
from dataclasses import dataclass
# from fig_dash.api.system.file.applications import FigDIconMap
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui import wrapFigDWindow, FigDAppContainer
# all app imports
from fig_dash.ui.apps.screenshot.screenshot import launch_screenshot_ui
# PyQt5 imports.
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QKeySequence, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QStringListModel, QPoint, QRectF, QTimer, QUrl, QDir, QMimeDatabase
from PyQt5.QtWidgets import QWidget, QAction, QScrollArea, QShortcut, QMainWindow, QApplication, QSplitter, QLabel, QToolBar, QToolButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QCompleter, QTabWidget, QGraphicsDropShadowEffect

def blank(): pass
AccentColorMap = {}
AppLauncherMap = {
    "screenshot": launch_screenshot_ui
}
AppIconMap = {
    "screenshot": FigD.icon("apps/screenshot/logo.png"),
}
ROW_SIZE = 4
# @dataclass
# class DashAppInfo:
#     name: str,
#     icon: str,
# class DashAppGroup(QWidget):
#     def __init__(self, apps: List[DashAppInfo], 
#                  parent: Union[QWidget, None]=None):
#         super(DashAppGroup, self).__init__()
class AppLauncherSearchBar(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(AppLauncherSearchBar, self).__init__(parent)
        # create actions.
        caseAction = self.addAction(
            FigD.Icon("browser/case.svg"), 
            QLineEdit.TrailingPosition
        )
        searchAction = self.addAction(
            FigD.Icon("browser/search.svg"), 
            QLineEdit.LeadingPosition
        )
        self.setStyleSheet("""
        QLineEdit {
            color: #fff;
            padding: 5px;
            background: #292929;
            border-radius: 5px;
        }""")
        self.setPlaceholderText("Search apps")
        completer = QCompleter()
        stringModel = QStringListModel()
        stringModel.setStringList(list(
            AppLauncherMap.keys()
        ))
        completer.setModel(stringModel)
        self.setCompleter(completer)
        self.setMinimumWidth(600)


class DashAppLauncher(QWidget): 
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashAppLauncher, self).__init__(parent)
        # vertical layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(10, 10, 10, 10)
        self.vboxlayout.setSpacing(10)
        # initialize scroll area (with buttons to launch apps.)
        self.searchbar = AppLauncherSearchBar()
        self.scroll_area = self.initScrollArea()
        # build layout.
        self.vboxlayout.addWidget(self.searchbar, 0, Qt.AlignCenter | Qt.AlignTop)
        self.vboxlayout.addWidget(self.scroll_area, 0, Qt.AlignCenter | Qt.AlignTop)
        self.vboxlayout.addStretch(1)
        # set layout.
        self.setLayout(self.vboxlayout)

    def initScrollArea(self):
        scroll_area = QScrollArea()
        launcher_widget = QWidget()
        launcher_widget.setStyleSheet("""
        QWidget {
            border-radius: 20px;
            background: #292929;
        }""")
        launcher_layout = QGridLayout()
        for i, app_name in enumerate(AppLauncherMap):
            accent_color = AccentColorMap.get(app_name, "gray")
            btn = QToolButton()
            btn.setText(app_name)
            btn.setIcon(FigD.Icon(
                AppIconMap[app_name]
            ))
            btn.setIconSize(QSize(90,90))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
            QToolButton {
                color: #fff; 
                border-radius: 10px;
                background: #484848;
                font-family: Be Vietnam Pro;
            }
            QToolButton:hover {
                border: 0px;
                color: #292929;
                font-weight: bold;
                background: """+accent_color+""";
            }""")
            btn.setFixedWidth(150)
            btn.setFixedHeight(150)
            btn.clicked.connect(
                AppLauncherMap[app_name]
            )
            launcher_layout.addWidget(btn, i//ROW_SIZE, i%ROW_SIZE)
        launcher_widget.setLayout(launcher_layout)
        scroll_area.setWidget(launcher_widget)
        scroll_area.setStyleSheet("""
        QScrollArea {
            background: transparent;
        }""")

        return scroll_area

def start_system_app_launcher():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    # create the clipboard UI widget.
    app = FigDAppContainer(sys.argv)
    app_launcher = DashAppLauncher()
    # wrap it in a FigDWindow
    # icon = FigDIconMap["app_launcher"]
    # accent_color = FigDAccentColorMap["app_launcher"]
    window = wrapFigDWindow(app_launcher, title="App Launcher and Store", 
                            accent_color=accent_color, icon=icon,
                            name="app_launcher")
    # show the app window.
    window.show()
    # run the application!
    app.exec()


if __name__ == "__main__":
    start_system_app_launcher()