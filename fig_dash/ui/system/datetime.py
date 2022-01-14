#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import jinja2
import datetime
from typing import Union
# fig-dash imports.
from fig_dash import FigD
# PyQt5 imports
from PyQt5.QtGui import QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QTabWidget, QToolBar, QLabel, QPushButton, QToolButton, QSizePolicy, QLineEdit, QHBoxLayout, QVBoxLayout, QAction, QCalendarWidget, QGraphicsDropShadowEffect, QApplication


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
    color: #eb5f34;
    font-size: 18px;
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 2px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 3px;
    margin-bottom: 3px;
    border-bottom: 4px solid #eb5f34;
    /* border-bottom: 4px solid #bf3636; */
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


class TimeZoneConverter(QWidget):
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


dash_calendar_style = '''
QTabWidget {
    color: #fff;
    border: 0px;
    background: transparent
}
QTabBar {
    background: transparent;
    padding: 2px;
    border: 0px;
}
QTabBar::tab {
    color: #fff;    
    border: 0px;
    font-size: 18px;
    
    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 2px;

    margin-top: 3px;
    margin-bottom: 3px;
}
QTabBar::tab:hover {
    color: #bf3636;
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop : 0.6 #eb5f34, stop: 0.9 #ebcc34); */
}
QTabBar::tab:selected {
    border: 0px;
    color: #eb5f34;
    font-size: 18px;

    padding-top: 2px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 2px;
    
    margin-top: 3px;
    margin-bottom: 3px;
    
    border-bottom: 4px solid #eb5f34;
    /* border-bottom: 4px solid #bf3636; */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
}'''
class Calendar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Calendar, self).__init__(parent)
        import time
        s = time.time()
        self.calendar_stylesheet = '''
        /* navigation bar */
        QCalendarWidget QWidget#qt_calendar_navigationbar {     
            background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }

        QCalendarWidget QToolButton {
            height: 25px;
            width: 120px;
            color: white;
            font-size: 18px;
            icon-size: 20px, 20px;
            background-color: transparent;
        }

        QCalendarWidget QMenu {
            width: 150px;
            left: 0px;
            color: white;
            font-size: 18px;
            background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 0.8), stop : 0.6 rgba(29, 29, 29, 0.6));
        }

        QCalendarWidget QMenu:selected {
            color: #292929;
            font-size: 18px;
            font-weight: bold;
            background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); 
        }

        QCalendarWidget QSpinBox { 
            width: 80px; 
            font-size: 18px; 
            text-align: center;
            color: white; 
            background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 0.8), stop : 0.6 rgba(29, 29, 29, 0.6));
            selection-background-color: blue;
            selection-color: rgb(255, 255, 255);
        }

        QCalendarWidget QSpinBox::up-button { 
            subcontrol-origin: border;  
            subcontrol-position: top right;  
            width: 20px; 
        }
        
        QCalendarWidget QSpinBox::down-button {
            subcontrol-origin: border; 
            subcontrol-position: bottom right;  
            width: 20px;
        }
        
        QCalendarWidget QSpinBox::up-arrow { 
            width: 20px;  
            height: 20px; 
        }
        
        QCalendarWidget QSpinBox::down-arrow { 
            width: 20px;  
            height: 20px; 
        }
        /* header row */
        QCalendarWidget QWidget { 
            alternate-background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 0.8), stop : 0.6 rgba(29, 29, 29, 0.6));
        }
        /* normal days */
        QCalendarWidget QAbstractItemView:enabled 
        {
            color: #eb5f34;  
            font-size: 18px;  
            background-color: #292929;
            border: 0px;
            selection-background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); 
            selection-color: #292929; 
        }
        
        QCalendarWidget QAbstractItemView {
            margin: 0px;
            background-color: #000;
        }

        /* days in other months */
        QCalendarWidget QAbstractItemView:disabled { 
            color: rgb(64, 64, 64);
        }'''
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0,0)
        shadow.setColor(QColor(235, 95, 52, 150))

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet(self.calendar_stylesheet)
        self.calendar.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.calendar, 0, Qt.AlignCenter)
        # print(f"set stylesheet in {time.time()-s}s")
        self.setLayout(self.layout)
        # self.setStyleSheet("""
        # QWidget { 
        #     background-image: url(/home/atharva/GUI/fig-dash/resources/icons/system/datetime/winter.jpg); 
        #     border: 0px;
        # }""")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.calendar.setFixedWidth(400)
        self.calendar.setMinimumHeight(400)
        # self.calendar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.setStyleSheet('''background: #292929; color: #fff;''')
class Schedule(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Schedule, self).__init__(parent)


class Reminders(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Reminders, self).__init__(parent)


class Holidays(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(Holidays, self).__init__(parent)


class MoonCalendar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(MoonCalendar, self).__init__(parent)


class DashCalendar(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashCalendar, self).__init__(parent)
        # create all the widgets
        self.calendar = Calendar(self)
        self.schedule = Schedule(self)
        self.holidays = Holidays(self) 
        self.reminders = Reminders(self)
        self.moon_calendar = MoonCalendar(self)
        # self.setElideMode(True)
        # add widgets to separate tabs.
        self.addTab(self.calendar, " "*2+"Calendar"+" "*2)
        self.addTab(self.schedule, " "*2+"Schedule"+" "*2)
        self.addTab(self.holidays, " "*1+"Holidays"+" "*1)
        self.addTab(self.reminders, " "*2+"Reminders"+" "*2)
        self.addTab(self.moon_calendar, " "*3+"Moon Calendar"+" "*3)
        self.setCurrentIndex(0)
        self.setStyleSheet(dash_calendar_style)


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
    # clockWidget.setGeometry(200, 200, 400, 600)
    app.exec()

def test_dash_calendar():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    # QFontDatabase.addApplicationFont(
    #     FigD.font("datetime/digital-7.ttf")
    # )
    import time
    s = time.time()
    # print("\x1b[31;1minitializing DashCalendar widget\x1b[0m")
    calendarWidget = DashCalendar()
    # print(f"\x1b[31;1minitializing DashCalendar in {time.time()-s}s\x1b[0m")
    s = time.time()
    # print(f"\x1b[31;1msetting attributes\x1b[0m")
    calendarWidget.setWindowFlags(Qt.WindowStaysOnTopHint)
    # calendarWidget.setAttribute(Qt.WA_TranslucentBackground)
    # print(f"\x1b[31;1mset attributes in {time.time()-s}s\x1b[0m")
    # print(f"\x1b[31;1mshowing DashCalendar\x1b[0m")
    calendarWidget.show()
    # print(f"\x1b[31;1msetting geometry\x1b[0m")
    calendarWidget.setGeometry(200, 200, 700, 600)
    # print(f"\x1b[31;1mexecuting application: starting event loop\x1b[0m")
    app.exec()


if __name__ == '__main__': 
    try:
        mode = sys.argv[1]
    except IndexError:
        exit("\x1b[31;1mIndexError:\x1b[0m You need provide [clock, calendar] as mode for testing one of them")
    if mode == "clock":
        test_dash_clock()
    elif mode == "calendar":
        test_dash_calendar()