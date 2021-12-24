#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2
import datetime
from typing import Union
# fig-dash imports.
from fig_dash import FigD
# PyQt5 imports
from PyQt5.QtGui import QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QTabWidget, QToolBar, QLabel, QPushButton, QToolButton, QSizePolicy, QLineEdit, QHBoxLayout, QVBoxLayout, QAction, QGraphicsDropShadowEffect, QApplication


dash_clock_style = '''
QTabWidget {
    color: #fff;
    border: 0px;
    background: transparent;
}
QTabBar {
    background: transparent;
    padding: 2px;
    border: 0px;
}
QTabBar::tab {
    border: 0px;
    color: #fff;
    font-size: 18px;
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 2px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 3px;
    margin-bottom: 3px;
    /* border-bottom: 4px solid #bf3636; */
}
QTabBar::tab:hover {
    color: #bf3636;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop : 0.6 #eb5f34, stop: 0.9 #ebcc34); */
}
QTabBar::tab:selected {
    border: 0px;
    color: #bf3636; /* #eb5f34; */
    font-size: 18px;
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 2px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 3px;
    margin-bottom: 3px;
    /* border-bottom: 4px solid #eb5f34; */
    border-bottom: 4px solid #bf3636;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
}'''
clock_style = '''
QWidget {
    color: #fff;
    border: 0px;
    font-size: 60px;
    background: transparent;
}
QToolButton {
    border: 0px;
    background: transparent;
}'''
class Clock(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Clock, self).__init__(parent)
        self.tod_ctr = 0
        self.layout = QVBoxLayout()
        # the clock backend.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)
        # create widgets.
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("digital-7"))
        self.timeOfDay = QPushButton(self)
        self.day = QLabel("")
        self.day.setAlignment(Qt.AlignCenter)
        self.day.setStyleSheet("font-size: 25px;")
        # add widgets to layout.
        self.layout.addWidget(self.timeOfDay, Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.day)
        self.layout.addStretch(1)
        # set style and layout.
        self.setLayout(self.layout)
        self.setStyleSheet(clock_style)

    def update(self):
        now = datetime.datetime.now()
        millis = int(now.strftime("%f")) % 1000
        time_str = datetime.datetime.strftime(now,
            f"%-I:%M:%S.<span style='font-size: 30px;'>{millis}</span> <span style='color: red; font-weight: bold;'>%p</span>"
        )
        if self.tod_ctr % 10 == 0:
            hr = int(now.strftime("%H"))
            self.setTimeOfDay(hr)
            self.setDay(now)
        self.tod_ctr += 1
        self.label.setText(time_str)

    def setDay(self, now: datetime.datetime):
        day = now.strftime("<span style='color: red; font-weight: bold;'>%A</span>, %-d %B %Y")
        self.day.setText(day)

    def setTimeOfDay(self, hr: int):
        timeOfDay = self.getTimeOfDay(hr)
        # print(timeOfDay)
        self.tod_icon = FigD.Icon(f"system/datetime/{timeOfDay}.png")
        # print(self.tod_icon)
        self.timeOfDay.setIcon(self.tod_icon)
        self.timeOfDay.setIconSize(QSize(150,150))

    def getTimeOfDay(self, hr: int):
        # print(hr)
        if 6 <= hr <= 11:
            timeOfDay = "morning"
        elif 11 <= hr <= 16:
            timeOfDay = "afternoon"
        elif 16 <= hr <= 19:
            timeOfDay = "evening"
        else:
            timeOfDay = "night"
        return timeOfDay


class Alarm(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Alarm, self).__init__(parent)


class StopWatch(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(StopWatch, self).__init__(parent)


class Timer(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Timer, self).__init__(parent)


class DashClock(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashClock, self).__init__(parent)
        # create all the widgets
        self.clock = Clock(self)
        self.alarm = Alarm(self)
        self.stopwatch = StopWatch(self)
        self.timer = Timer(self)
        # add widgets to separate tabs.
        self.addTab(self.clock, "Clock")
        self.addTab(self.alarm, "Alarm")
        self.addTab(self.stopwatch, "Stopwatch")
        self.addTab(self.timer, "Timer")
        self.setCurrentIndex(0)
        self.setStyleSheet(dash_clock_style)


def test_dash_clock():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(
        FigD.font("datetime/digital-7.ttf")
    )
    clockWidget = DashClock()
    clockWidget.setWindowFlags(Qt.WindowStaysOnTopHint)
    clockWidget.setAttribute(Qt.WA_TranslucentBackground)
    clockWidget.show()
    clockWidget.setGeometry(200, 200, 400, 600)
    app.exec()


class DashCalendar(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashCalendar, self).__init__(parent)


if __name__ == '__main__': 
    test_dash_clock()