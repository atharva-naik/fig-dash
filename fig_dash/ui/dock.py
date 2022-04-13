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
from PyQt5.QtGui import QColor, QPalette, QPen, QBrush, QPolygon, QPainter, QRegion, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QPoint, QPointF, QUrl, QEvent, QStringListModel, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QAction, QMainWindow, QToolButton, QLineEdit, QHBoxLayout, QVBoxLayout #, QDockWidget 


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
        self.audioStreamsBtn = self.initDockBtn(icon="dock/audio_tracks.svg", icon_size=[40,40])
        self.settingsBtn = self.initDockBtn(icon="dock/settings.svg", icon_size=[40,40])
        self.taskviewBtn = self.initDockBtn(icon="dock/taskview.svg", icon_size=[35,35])
        self.powerBtn = self.initDockBtn(icon="dock/power.svg", icon_size=[35,35])
        self.webBtn = self.initDockBtn(icon="dock/web.svg", icon_size=[35,35])
        self.aiBtn = self.initDockBtn(icon="dock/cortana.svg", icon_size=[35,35])
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
        self.addBlank()
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
        self.addBlank()
        # add widgets to layout.
        self.setLayout(self.layout)

    def addBlank(self, width=10):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        widget.setFixedWidth(width)
        self.layout.addWidget(widget)

    def initDockBtn(self, **args):
        dockBtn = DockWidgetBtn(**args)

        return dockBtn


class DashDockWidget(QMainWindow):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashDockWidget, self).__init__(parent)
        self.ui = DockWidgetUI()
        self.setCentralWidget(self.ui)
        # self.ui.setFixedHeight(30)
        self.w = 800
        self.h = 50 
        self.setFixedWidth(self.w)
        self.setFixedHeight(self.h)
        self.setWindowOpacity(0.8)
        self.setStyleSheet("""
        QMainWindow {
            padding-top: 0px;
            padding-bottom: 0px;
            border-radius: 10px;
            background: transparent;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9)); */
        }""")
        # point1 = QPoint(40, 0)
        # point2 = QPoint(0, 50)
        # point3 = QPoint(800, 50)
        # point4 = QPoint(760, 0)
        # poly = QPolygon((point1, point2, point3, point4))
        # mask = QRegion(poly)
        # self.setMask(mask)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(QPen(
            QBrush(QColor(0,0,0,1)), 
            0
        ))
        # linear gradient.
        lgrad = QLinearGradient(QPointF(0, 0), QPointF(0, 60))
        for i in range(8):
            c = 17+i*5
            if i <= 2:
                alpha = 0
            else:
                alpha = int(255*0.7)
            print(c, c, c, alpha)
            stop = min(0.143*i, 1)
            lgrad.setColorAt(stop, QColor(c, c, c, alpha))
        # lgrad.setColorAt(0.143, QColor(22, 22, 22, int(255*0.9)))
        # lgrad.setColorAt(0.286, QColor(27, 27, 27, int(255*0.9)))
        # lgrad.setColorAt(0.429, QColor(32, 32, 32, int(255*0.9)))

        painter.setBrush(lgrad)
        h = self.h
        w = self.w
        point1 = QPoint(50, 0)
        point2 = QPoint(0, h-5)
        point3 = QPoint(0, h)
        point4 = QPoint(w, h)
        point5 = QPoint(w, h-5)
        point6 = QPoint(w-50, 0)
        # point5 = QPoint(0, 20)
        poly = QPolygon((point1, point2, point3, point4, point5, point6))
        painter.drawPolygon(poly)
        
        