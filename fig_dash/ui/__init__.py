#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
from pathlib import Path
# fig-dash imports.
from fig_dash import FigD
# PyQt5 imports
# from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QToolButton, QVBoxLayout, QHBoxLayout


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
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}""")
DASH_WIDGET_GROUP = jinja2.Template("""
""")
class DashWidgetGroupBtn(QToolButton):
    '''File viewer button'''
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashWidgetGroupBtn, self).__init__(parent)
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        self.hover_response = "background"
        if "icon" in args:
            self.inactive_icon = os.path.join("system/fileviewer", args["icon"])
            stem, ext = os.path.splitext(Path(args["icon"]))
            active_icon = f"{stem}_active{ext}"
            self.active_icon = os.path.join("system/fileviewer", active_icon)
            if os.path.exists(FigD.icon(self.active_icon)):
                self.hover_response = "foreground"
            self.setIcon(FigD.Icon(self.inactive_icon))
        elif "text" in args:
            self.setText(args["text"])
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStatusTip(tip)
        if self.hover_response == "background":
            self.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: transparent;
            }
            QToolButton:hover {
                color: #292929;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''')
        else:
            self.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: transparent;
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
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(2)
        self.group.setLayout(self.layout)
        layout.addWidget(self.Label(name))
        layout.addWidget(self.group)
        layout.addStretch(1)
        self.setLayout(layout)

    def Label(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            padding: 6px;
            color: #69bfee;
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }''')
        return name

    def initBtnGroup(self, btn_args, 
                     orient="horizontal"):
        btnGroup = QWidget()
        btnGroup.btns = []
        if orient == "horizontal":
            layout = QHBoxLayout()
        elif orient == "vertical":
            layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        btnGroup.layout = layout
        btnGroup.setLayout(layout)
        btnGroup.setStyleSheet('''
        QWidget {
            color: #fff;
            border: 0px;
            background: transparent;
        }''')
        layout.addStretch(1)
        for args in btn_args:
            btn = self.initBtn(**args)
            btnGroup.btns.append(btn)
            layout.addWidget(btn, 0, Qt.AlignCenter)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def initBtn(self, **args):
        return DashWidgetGroupBtn(self, **args)