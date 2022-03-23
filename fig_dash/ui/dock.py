#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dock (hopefully like latte dock).
import json
import jinja2
import numpy as np
from typing import Union
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.browser.url.parse import UrlOrQuery
# PyQt5 imports
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QPoint, QUrl, QEvent, QStringListModel, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QAction, QDockWidget, QToolButton, QLineEdit, QHBoxLayout, QVBoxLayout


class DockWidgetAppBtn(QToolButton):
    pass


dock_widget_btn_style = """
QToolButton {
    color: #fff;
    border: 0px;
    background: transparent;
}
"""
class DockWidgetBtn(QToolButton):
    def __init__(self, **args):
        super(DockWidgetBtn, self).__init__()
        icon = args.get("icon")
        self.icon_size = args.get("icon_size", [30,30])
        self.zoom_factor = args.get("zoom_factor", 1.3)
        self.setIcon(FigD.Icon(icon))
        self.setIconSize(QSize(*self.icon_size))
        self.setStyleSheet(dock_widget_btn_style)

    def leaveEvent(self, event):
        self.setIconSize(QSize(*self.icon_size))
        super(DockWidgetBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        zoomed_icon_size = self.zoom_factor*np.array(self.icon_size) 
        zoomed_icon_size = zoomed_icon_size.tolist()
        self.setIconSize(QSize(*zoomed_icon_size))
        super(DockWidgetBtn, self).enterEvent(event)


class DockSearchBar(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DockSearchBar, self).__init__(parent)
        self.setFixedHeight(35)
        self.setFixedWidth(350)
        palette = self.palette()
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128,128,128))
        palette.setColor(QPalette.Base, QColor(29,29,29,255))
        palette.setColor(QPalette.Text, QColor(255,255,255))
        palette.setColor(QPalette.Window, QColor(29,29,29,255))
        palette.setColor(QPalette.WindowText, QColor(255,255,255,255))
        self.setPlaceholderText("Search on PC")
        self.setPalette(palette)
        self.searchAction = QAction()
        self.searchAction.setIcon(FigD.Icon("dock/search.svg"))
        self.addAction(self.searchAction, self.LeadingPosition)


class DockWidgetUI(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DockWidgetUI, self).__init__(parent)
        self.searchbar = DockSearchBar()
        # layout.
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        # create buttons.
        self.audioStreamsBtn = self.initDockBtn(icon="dock/audio_tracks.svg",icon_size=[35,35])
        self.settingsBtn = self.initDockBtn(icon="dock/settings.svg", icon_size=[35,35])
        self.taskviewBtn = self.initDockBtn(icon="dock/taskview.svg")
        self.powerBtn = self.initDockBtn(icon="dock/power.svg")
        self.webBtn = self.initDockBtn(icon="dock/web.svg")
        self.aiBtn = self.initDockBtn(icon="dock/cortana.svg")
        self.setObjectName("DockWidgetUI")
        # color the palette.
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(29,29,29,255))
        palette.setColor(QPalette.Text, QColor(255,255,255))
        palette.setColor(QPalette.Window, QColor(29,29,29,255))
        # palette.setColor(QPalette.WindowText, QColor(255,255,255,255))
        self.setPalette(palette)
        # self.setStyleSheet("""
        # QWidget {
        #     background: black;
        # }""")
        # populate layout.
        self.layout.addWidget(self.powerBtn)
        self.layout.addWidget(self.searchbar)
        # cortana like AI button.
        self.layout.addWidget(self.aiBtn)
        # waveform readout.
        self.layout.addWidget(self.taskviewBtn)
        # current app buttons.
        self.layout.addWidget(self.webBtn)
        self.layout.addStretch(1)
        self.layout.addWidget(self.audioStreamsBtn)
        self.layout.addWidget(self.settingsBtn)
        # add widgets to layout.
        self.setLayout(self.layout)

    def initDockBtn(self, **args):
        dockBtn = DockWidgetBtn(**args)

        return dockBtn


class DashDockWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashDockWidget, self).__init__(parent)
        self.ui = DockWidgetUI()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)
        # self.setStyleSheet("""
        # QWidget {
        #     background: black;
        # }""")
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(29,29,29,255))
        palette.setColor(QPalette.Text, QColor(255,255,255))
        palette.setColor(QPalette.Window, QColor(29,29,29,255))
        # palette.setColor(QPalette.WindowText, QColor(255,255,255,255))
        self.setPalette(palette)