#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::system::sysutils")
# titlebar for the main window
import os
import sys
import jinja2
from typing import Union
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.system.battery import Battery
# PyQt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QToolBar, QToolButton, QSizePolicy, QVBoxLayout, QGraphicsDropShadowEffect
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
sysutils_bar_style = jinja2.Template('''
QWidget { 
    color: #fff;
    border: 0px;
    background: red;
}''')
sysutils_btn_style = '''
QToolButton {
    font-family: Helvetica;
    border-radius: 20px; 
}  
'''
class SysUtilsBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget], icon, **kwargs):
        super(SysUtilsBtn, self).__init__(parent)
        self.setToolTip(kwargs.get("tip", "a tip"))
        self.inactive_icon = icon
        stem, ext = os.path.splitext(icon)
        self.active_icon = stem+"_active"+ext
        self.setIcon(FigD.Icon(self.inactive_icon))
        size = kwargs.get("size", (40,40))
        self.setIconSize(QSize(*size))
        self.clicked.connect(kwargs.get("callback", self.callback))
        self.setStyleSheet(sysutils_btn_style)

    def enterEvent(self, event):
        # print(f"entered {self.inactive_icon}")
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setColor(QColor(235, 95, 52))
        # set active icon only if it exists.
        if os.path.exists(FigD.icon(self.active_icon)):
            self.setIcon(FigD.Icon(self.active_icon))
            super(SysUtilsBtn, self).enterEvent(event)
            glow_effect.setBlurRadius(10)
            glow_effect.setOffset(5,5)
        else:
            glow_effect.setBlurRadius(5)
            glow_effect.setOffset(0,0)

        self.setGraphicsEffect(glow_effect)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)
        # print(f"left {self.inactive_icon}")
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(SysUtilsBtn, self).leaveEvent(event)

    def callback(self):
        pass


class SysUtilsBar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(SysUtilsBar, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.ideasJarBtn = SysUtilsBtn(
            parent=self,
            icon="widget/ideas/ideas_jar.svg",
            tip="your bottled ideas",
            size=(70,70),
        )
        self.onScreenKeyboardBtn = SysUtilsBtn(
            parent=self,
            icon="system/sysutils/onscreenkeyboard.svg", 
            tip="open on screen keyboard.",
        )
        self.trashBtn = SysUtilsBtn(
            parent=self,
            icon="system/sysutils/trash.svg", 
            tip="open trash viewer.",
        )
        self.transBtn = SysUtilsBtn(
            parent=self,
            icon="system/sysutils/trans.svg", 
            tip="open translation utility.",
        )
        self.ttsBtn = SysUtilsBtn(
            parent=self,
            icon="system/sysutils/tts.svg", 
            tip="open text to speech.",
        )
        # self.fileExplorerBtn = SysUtilsBtn(
        #     parent=self,
        #     icon="system/sysutils/file_explorer.svg", 
        #     tip="toggle file explorer.",
        # )
        self.systemMonitorBtn = SysUtilsBtn(
            parent=self,
            icon="system/sysutils/system_monitor.svg", 
            tip="view system information",
        )
        # add buttons.
        self.layout.addWidget(self.ideasJarBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.onScreenKeyboardBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.systemMonitorBtn, 0, Qt.AlignCenter)
        # self.layout.addWidget(self.fileExplorerBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.transBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.ttsBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.trashBtn, 0, Qt.AlignCenter)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
    # def connectWindow(self, dash_window):
    #     self.dash_window = dash_window
    #     self.calendarBtn.clicked.connect(dash_window.datetime_notifs_splitter.toggle)
    #     self.clockBtn.clicked.connect(dash_window.datetime_notifs_splitter.toggle)
    #     self.ideasBtn.clicked.connect(dash_window.ideas.toggle)
    #     self.weatherBtn.clicked.connect(dash_window.weather.toggle)
    def toggle(self):
        '''toggle visibility of system utilities panel.'''
        if self.isVisible(): self.hide()
        else: self.show()

    def connectTitleBar(self, titlebar):
        pass
        # self.titlebar = titlebar
        # self.titlebar.sysUtilsBtn.clicked.connect(self.toggle)

    def initBtn(self, icon, **kwargs):
        btn = QToolButton(self)
        btn.setToolTip(kwargs.get("tip", "a tip"))
        btn.setIcon(FigD.Icon(icon))
        size = kwargs.get("size", (40,40))
        btn.setIconSize(QSize(*size))
        btn.clicked.connect(kwargs.get("callback", self.callback))
        btn.setStyleSheet(sysutils_btn_style)
        
        return btn
# def test_sysutilsbar():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     sysutils_bar = SysUtilsBar(window)
#     window.addToolBar(Qt.TopToolBarArea, sysutils_bar)
#     window.show()
#     sys.exit(app.exec_())
# if __name__ == '__main__':
#     test_sysutilsbar()