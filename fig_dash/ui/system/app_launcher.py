#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import *
from pathlib import Path
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.titlebar import WindowTitleBar
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
from fig_dash.ui import DashWidgetGroup, FigDAppContainer, wrapFigDWindow#, extract_colors_from_qt_grad, create_css_grad
# all system imports.
from fig_dash.ui.system.terminal import launch_terminal
from fig_dash.ui.system.clipboard import launch_clipboard
from fig_dash.ui.system.fileviewer import launch_fileviewer
from fig_dash.ui.widget.codemirror import launch_codemirror
from fig_dash.ui.system.imageviewer import launch_imageviewer
# PyQt5 imports.
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QKeySequence, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QStringListModel, QPoint, QRectF, QTimer, QUrl, QDir, QMimeDatabase
from PyQt5.QtWidgets import QWidget, QAction, QScrollArea, QShortcut, QMainWindow, QApplication, QSplitter, QLabel, QToolBar, QToolButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QCompleter, QTabWidget, QGraphicsDropShadowEffect

def blank(): pass
FIgDSystemAppLauncherMap = {
    "clipboard": launch_clipboard,
    "fileviewer": launch_fileviewer,
    "imageviewer": launch_imageviewer,
    "videoplayer": blank,
    "codeeditor": launch_codemirror,
    "terminal": launch_terminal,
}
ROW_SIZE = 4

class SystemAppLauncherSearchBar(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(SystemAppLauncherSearchBar, self).__init__(parent)
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
        self.setPlaceholderText("Search system apps")
        completer = QCompleter()
        stringModel = QStringListModel()
        stringModel.setStringList(list(
            FIgDSystemAppLauncherMap.keys()
        ))
        completer.setModel(stringModel)
        self.setCompleter(completer)
        self.setMinimumWidth(600)
        self.setClearButtonEnabled(True)


class DashSystemAppLauncher(QWidget): 
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashSystemAppLauncher, self).__init__(parent)
        # vertical layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(10, 10, 10, 10)
        self.vboxlayout.setSpacing(10)
        # initialize scroll area (with buttons to launch apps.)
        self.searchbar = SystemAppLauncherSearchBar()
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
        for i, app_name in enumerate(FIgDSystemAppLauncherMap):
            accent_color = FigDAccentColorMap[app_name]
            btn = QToolButton()
            btn.setText(app_name)
            btn.setIcon(FigD.Icon(
                FigDSystemAppIconMap[app_name]
            ))
            btn.setIconSize(QSize(90,90))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
            QToolButton {
                color: #fff; 
                border-radius: 10px;
                background: #484848;
                font-family: 'Be Vietnam Pro', sans-serif;
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
                FIgDSystemAppLauncherMap[app_name]
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
    app_launcher = DashSystemAppLauncher()
    # wrap it in a FigDWindow
    def blank(): pass
    icon = FigDSystemAppIconMap["app_launcher"]
    accent_color = FigDAccentColorMap["app_launcher"]
    window = wrapFigDWindow(app_launcher, title="System App Launcher", 
                            accent_color=accent_color, icon=icon,
                            name="app_launcher", add_tabs=False,
                            titlebar_callbacks={
                                "viewSourceBtn": blank(),
                            })
    # show the app window.
    window.show()
    # run the application!
    app.exec()


if __name__ == "__main__":
    start_system_app_launcher()