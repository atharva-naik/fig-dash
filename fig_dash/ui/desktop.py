#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::desktop")
import os
import sys
from textwrap import wrap
from typing import *
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui import FigDAppContainer
# PyQt5 imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout

# dash desktop widget.
class DashDesktopWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(DashDesktopWidget, self).__init__(parent)

# desktop window
class FigDesktopWindow(QMainWindow):
    def __init__(self):
        super(FigDesktopWindow, self).__init__()
        centralWidget = QWidget()
        centralWidget.setObjectName("FigDCentralWidget")
        centralWidget.setStyleSheet("""
        QWidget#FigDCentralWidget {
            color: #fff;
            background: transparent;
            font-family: "Be Vietnam Pro";
        }""")   
        # layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        # desktop.
        self.desktop = DashDesktopWidget()
        # build layout.
        self.vboxlayout.addWidget(self.desktop)
        # set layout.
        centralWidget.setLayout(self.vboxlayout)
        # set central widget.
        self.setCentralWidget(centralWidget)
        # window flags: frameless, always on top.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def openWindow(self):
        from fig_dash.ui.system.imageviewer import imageviewer_mdi_subwindow_factory
        sub_window = imageviewer_mdi_subwindow_factory()
        self.desktop.addSubWindow(sub_window)
        sub_window.show()

# test desktop.
def test_desktop():
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    desktop = FigDesktopWindow()
    desktop.showMaximized()
    desktop.openWindow()
    app.exec()

if __name__ == "__main__":
    test_desktop()