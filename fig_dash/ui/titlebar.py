#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# titlebar for the main window
import sys
import jinja2
from typing import Union
# fig-dash imports.
from fig_dash import FigD
# PyQt5 imports
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QToolBar, QToolButton, QMainWindow, QSizePolicy


# title_bar_style = '''
# QToolBar {
#     margin: 0px; 
#     border: 0px; 
#     color: #fff;
#     /* border-top-left-radius: 5px; */
#     /* border-top-right-radius: 5px; */
#     background: #000;
#     /* background: url('''+f"'{FigD.icon('''titlebar/texture.png''')}'"+''');  */
#     /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929); */    
# }
title_bar_style = jinja2.Template('''
QToolBar {
    margin: 0px; 
    border: 0px; 
    color: #fff;
    /* border-top-left-radius: 5px; */
    /* border-top-right-radius: 5px; */
    /* background: #000; */
    background: url({{ TITLEBAR_BACKGROUND_URL }})
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929); */    
}
''')
title_btn_style = '''
QToolButton {
    font-family: Helvetica;
    border-radius: 12px; 
}
QToolButton:hover {
    background: rgba(255, 255, 255, 0.5);
    /* background: rgba(255, 223, 97, 0.5); */
}   
'''
class TitleBar(QToolBar):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(TitleBar, self).__init__("Titlebar", parent)
        self.setStyleSheet(title_bar_style.render(
            TITLEBAR_BACKGROUND_URL=FigD.icon("titlebar/texture.png")
        ))
        self.setIconSize(QSize(22,22))
        self.setMovable(False)
        # close window
        self.closeBtn = self.initTitleBtn(
            "titlebar/close.svg", 
            tip="close window",
            callback=self.callback if parent is None else parent.close
        )
        # minimize window
        self.minimizeBtn = self.initTitleBtn(
            "titlebar/minimize.svg", 
            tip="minimize window",
            callback=self.callback if parent is None else parent.showMinimized
        )
        # maximize button
        self.maximizeBtn = self.initTitleBtn(
            "titlebar/maximize.svg", 
            tip="maximize window",
            callback=self.callback if parent is None else self.maximize
        )
        # window title
        self.title = QLabel()
        self.title.setText("ScriptO: New Project")
        self.title.setStyleSheet("color: #fff; font-size: 16px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # left_spacer = QWidget()
        # left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # right_spacer = QWidget()
        # right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(self.closeBtn)
        self.addWidget(self.minimizeBtn)
        self.addWidget(self.maximizeBtn)
        self.addWidget(self.initSpacer())
        self.addWidget(self.title)
        self.addWidget(self.initSpacer())
        self.addWidget(self.initTitleBtn(""))
        self.addWidget(self.initTitleBtn(""))
        self.addWidget(self.initTitleBtn(""))
        self.setMaximumHeight(30)

    def maximize(self):
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            if parent.isMaximized():
                parent.showNormal()
            else:
                parent.showMaximized()

    def initSpacer(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        return spacer

    def initTitleBtn(self, icon, **kwargs):
        btn = QToolButton(self)
        btn.setToolTip(kwargs.get("tip", "a tip"))
        btn.setIcon(FigD.Icon(icon))
        btn.setIconSize(QSize(22,22))
        btn.clicked.connect(kwargs.get("callback", self.callback))
        btn.setStyleSheet(title_btn_style)

        return btn

    def callback(self):
        pass

    def mousePressEvent(self, event):
        parent = self.parent()
        if parent is None: return
        parent.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        parent = self.parent()
        if parent is None: return
        delta = QPoint(event.globalPos() - parent.oldPos)
        parent.move(parent.x() + delta.x(), parent.y() + delta.y())
        parent.oldPos = event.globalPos()


def titlebar_test():
    app = QApplication(sys.argv)
    window = QMainWindow()
    titlebar = TitleBar(window)
    window.addToolBar(Qt.TopToolBarArea, titlebar)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    titlebar_test()