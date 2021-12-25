#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2
import datetime
from typing import Union
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.system.battery import Battery
# PyQt5 imports
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QToolBar, QToolButton, QDialog, QSizePolicy, QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, QTextEdit, QScrollArea


notif_style = '''
QWidget {
    border: 0px;
    color: #fff;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
}
QToolButton {
    border: 0px;
    background: transparent;
}'''
notif_panel_style = ''''''
notif_dialog_style = ''''''
class NotifDialog(QDialog):
    pass


class Notification(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(Notification, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # set app name.
        self.appName = QLabel(args.get("name", "An app"))
        # self.appName.setAlignment(Qt.AlignCenter)
        self.appName.setStyleSheet('''
        QLabel {
            border: 0px;
            color: #eb5f34;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
        }''')
        # set app icon.
        self.appIcon = QToolButton(self)
        self.appIcon.setIcon(QIcon(args.get("icon")))
        self.appIcon.setIconSize(QSize(40,40))
        self.appIcon.setAttribute(Qt.WA_TranslucentBackground)
        # notif time.
        self.timeLabel = QLabel(args.get("time"))
        self.timeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.timeLabel.setStyleSheet('''
        QLabel {
            color: gray;
            border: 0px;
            font-size: 14px;
            background: transparent;
        }''')
        # button to dismiss notif.
        self.dismissBtn = QToolButton(self)
        self.dismissBtn.setIcon(FigD.Icon("widget/notifs/close.svg"))
        # self.dismissBtn.clicked.connect(self.close)
        self.dismissBtn.setFixedSize(QSize(40,40))
        self.dismissBtn.setIconSize(QSize(20,20))
        self.dismissBtn.setAttribute(Qt.WA_TranslucentBackground)
        # reference to the notification object.
        self.dismissBtn.notif = self
        # create notification header.
        self.header = QWidget()
        self.headerBox = QHBoxLayout()
        self.headerBox.setContentsMargins(0, 0, 0, 0)
        self.headerBox.addWidget(self.appIcon)
        self.headerBox.addWidget(self.appName)
        self.headerBox.addWidget(self.timeLabel) 
        self.headerBox.addWidget(self.dismissBtn)
        self.header.setLayout(self.headerBox)
        self.layout.addWidget(self.header)
        # set notif message.
        self.content = QTextEdit()
        self.content.setHtml(args.get("msg"))
        self.content.setMaximumHeight(100)
        self.content.setMinimumHeight(60)
        self.content.setReadOnly(True)
        self.content.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.content.setStyleSheet('''
        QTextEdit {
            color: #fff;
            border: 0px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));  
        }''')
        # self.content.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.addWidget(self.content)
        # add shadow to give 3D appearance.
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        self.setStyleSheet(notif_style)
        # apply glow effect for 3D appearance.
        self.setGraphicsEffect(glow_effect)
        # set layout.
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class NotifsPanel(QScrollArea):
    '''Notifications panel.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(NotifsPanel, self).__init__(parent)
        # layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)        
        self.box = QWidget()
        self.boxLayout = QVBoxLayout()
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.setSpacing(2)
        self.box.setLayout(self.boxLayout)
        self.boxLayout.addStretch(1)
        self.setStyleSheet('''
        QWidget {
            border: 0px;
            background: transparent;
        }''')
        # layout.addStretch(1)
        # layout.addWidget(self.box)
        # self.setLayout(layout)
        self.setWidget(self.box)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        

    def popNotif(self, i: int):
        pass

    def dismiss(self):
        sendingBtn = self.sender()
        notif = sendingBtn.notif
        # print(sendingBtn)
        notif.close()

    def pushNotif(self, **args):
        now = datetime.datetime.now()
        time = now.strftime("%a, %b %d  %-I:%M %p")
        notif = Notification(self, time=time, **args)
        notif.dismissBtn.clicked.connect(self.dismiss)
        self.boxLayout.insertWidget(1, notif)

def test_notifs():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    notifs_panel = NotifsPanel()
    notifs_panel.pushNotif(
        name="ScriptO",
        icon="/home/atharva/GUI/scripto/logo.png",
        msg="This is a notification from <b>ScriptO</b>",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="Upgrade to <b><i>premium</i></b> version for benefits",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="A notification",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="Yet another notification",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="Damn it, another notification :(",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="Damn it, another notification :(",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="Damn it, another notification :(",
    )
    notifs_panel.pushNotif(
        name="FigUI",
        icon="/home/atharva/GUI/FigUI/logo.png",
        msg="Damn it, another notification :(",
    )
    # notifs_panel.pushNotif(
    #     name="ScriptO",
    #     icon="/home/atharva/GUI/scripto/logo.png",
    #     msg="This is a notification from <b>ScriptO</b>",
    # )
    notifs_panel.show()
    notifs_panel.resize(500, 500)
    app.exec()


if __name__ == '__main__':
    test_notifs()