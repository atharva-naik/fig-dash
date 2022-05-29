#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::system::visualizer")
import os
import jinja2
from typing import Union
from functools import partial
# fig-dash imports.
from fig_dash.utils import *
from fig_dash.assets import FigD
# PyQt5 imports
from PyQt5.QtGui import QColor, QPainter, QPen, QFontDatabase, QKeySequence
from PyQt5.QtCore import Qt, QSize, QPoint, QUrl, QEvent
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtWidgets import QWidget, QLabel, QToolBar, QMainWindow, QApplication, QVBoxLayout, QShortcut


class DiskUtilization(QWidget):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(DiskUtilization, self).__init__(parent)
        self.series = QPieSeries()
        self.series.append("Desktop", 80)
        self.series.append("Music", 80)
        self.series.append("Videos", 100)
        self.series.append("Pictures", 200)
        self.series.append("Downloads", 500)
        self.series.append("Other", 50)
        # adding slice.
        # self.slice = QPieSlice()
        self.slice = self.series.slices()[2]
        self.slice.setExploded(True)
        self.slice.setLabelVisible(True)
        self.slice.setPen(QPen(Qt.green, 2))
        self.slice.setBrush(Qt.green)

        color_series = sampleRGBSeries(len(self.series), width=40)
        for i in range(len(self.series)):
            # if i == 2: continue
            # self.series.slices()[i].brush().color()
            color = QColor(*color_series[i])
            pen = QPen(color, 0)
            pen.setWidth(0)
            self.series.slices()[i].setBrush(color)
            self.series.slices()[i].setPen(pen)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Disk Utilization")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.setBackgroundVisible(False)
        # self.chart.setAttribute(Qt.WA_TranslucentBackground)
        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.chartview.setFixedHeight(600)
        self.chartview.setFixedWidth(600)
        # self.chartview.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.chartview.setStyleSheet("""
        # QMainWindow {
        #     border: 0px;
        #     background: transparent;
        # }""")
        # self.chartview.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.chartview, 0, Qt.AlignCenter | Qt.AlignBottom)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
        }""")


class DashSystemMonitor(QMainWindow):
    def __init__(self, ):
        super(DashSystemMonitor, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("""
        QMainWindow {
            border: 0px;
            background: transparent;
        }""")
        self.disk_utilization = DiskUtilization()
        self.setCentralWidget(self.disk_utilization)
        self.Esc = QShortcut(QKeySequence("Esc"), self)
        self.Esc.activated.connect(self.close)
        # self.setCentralWidget(QLabel("System Monitor"))

def test_system_monitor():
    import sys
    # import platform
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    system_monitor = DashSystemMonitor(
        # clipboard=app.clipboard(),
        #  background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        # logo="system/fileviewer/logo.svg",
        # font_color="#fff",
    )
    QFontDatabase.addApplicationFont(
        FigD.font("BeVietnamPro-Regular.ttf")
    )
    # system_monitor.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    system_monitor.setWindowFlags(Qt.WindowStaysOnTopHint)
    system_monitor.showMaximized()
    # system_monitor.statusBar().addWidget()
    # app.setWindowIcon(FigD.Icon("system/fileviewer/logo.svg"))
    app.exec()


if __name__ == "__main__":
    test_system_monitor()