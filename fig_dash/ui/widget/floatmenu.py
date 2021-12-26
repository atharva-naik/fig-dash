#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2
from typing import Union
# Qt5 imports.
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QApplication, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
# fig-dash imports.
from fig_dash.assets import FigD


floatmenu_style = '''
'''
floatmenu_btn_style = jinja2.Template('''
QWidget {
    background: transparent;
}
QToolButton {
    margin-right: 5px;
    margin-bottom: 5px;
    padding: 10px;
    color: #292929;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
    border-radius: 34px;
}
QToolButton:hover {
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(235, 95, 52, 0.8), stop : 0.6 rgba(235, 204, 52, 0.9));
}''')
class FloatMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FloatMenu, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # weather button.
        self.weatherBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/weather.png"),
            tip="View today's weather and weekly forecast.",
            size=QSize(45,45),
        )
        self.calendarBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/calendar.png"),
            tip="Calendar widget.",
            size=QSize(45,45),
        )
        self.clockBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/clock.png"),
            tip="Clock, timer, stopwatch and other widgets.",
            size=QSize(45,45),
        )
        self.whiteboardBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/whiteboard.png"),
            tip="Need to explain something? Present your ideas on a whiteboard.",
            size=QSize(45,45),
        )
        self.kanbanBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/kanban.jpg"),
            tip="Organize your project with a kanban board.",
            size=QSize(45,45),
        )
        self.notesBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/notes.png"),
            tip="Add new notes.",
            size=QSize(45,45),
        )
        self.ideasBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/ideas.png"),
            tip="Have an idea? write it down. Tell me when I should remind you.",
            size=QSize(45,45),
        )
        self.newsBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/news.png"),
            tip="Discover news and tune your feed to suit your interests.",
            size=QSize(45,45),
        )
        self.botBtn = self.initMenuBtn(
            icon=FigD.Icon("widget/floatmenu/bot.png"),
            tip="Bot assistant to help you out with productivity.",
            size=QSize(45,45),
        )
        # add buttons.
        self.layout.addWidget(self.weatherBtn)
        self.layout.addWidget(self.calendarBtn)
        self.layout.addWidget(self.clockBtn)
        self.layout.addWidget(self.whiteboardBtn)
        self.layout.addWidget(self.kanbanBtn)
        self.layout.addWidget(self.notesBtn)
        self.layout.addWidget(self.ideasBtn)
        self.layout.addWidget(self.newsBtn)
        self.layout.addWidget(self.botBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def connectWindow(self, dash_window):
        self.dash_window = dash_window
        self.calendarBtn.clicked.connect(dash_window.datetime_notifs_splitter.toggle)
        self.clockBtn.clicked.connect(dash_window.datetime_notifs_splitter.toggle)
        self.ideasBtn.clicked.connect(dash_window.ideas.toggle)
        self.weatherBtn.clicked.connect(dash_window.weather.toggle)

    def toggle(self):
        '''toggle visibility of dashboard widgets.'''
        if self.isVisible(): 
            self.hide()
        else: 
            self.show()

    def initMenuBtn(self, **args):
        btn = QToolButton(self)
        btn.setIcon(args.get("icon"))
        btn.setIconSize(
            args.get(
                "size", 
                QSize(20,20)
            )
        )
        btn.setToolTip(args.get("tip", "a tip."))
        btn.setStyleSheet(
            floatmenu_btn_style.render(

            )
        )
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        btn.setGraphicsEffect(glow_effect)

        return btn


def test_floatmenu():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    floatmenu = FloatMenu()
    floatmenu.setAttribute(Qt.WA_TranslucentBackground)
    floatmenu.show()
    app.exec()


if __name__ == '__main__':
    test_floatmenu()