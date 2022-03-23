#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# titlebar for the main window
from gc import callbacks
import sys
import jinja2
from typing import Union
# fig-dash imports.
from fig_dash import FigD
from fig_dash.api.system.battery import Battery
from fig_dash.api.system.network import NetworkHandler
# PyQt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QKeySequence, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QSlider, QWidget, QApplication, QLabel, QLineEdit, QToolBar, QToolButton, QMainWindow, QShortcut, QSizePolicy, QHBoxLayout
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
battery = jinja2.Template('''
<svg xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:rgb(200,255,0);stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:rgb(0,255,0);stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:rgb(255,145,66);stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:rgb(255,170,0);stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
        </linearGradient>
    </defs>
    <g>
      <rect x="0" y="0" stroke="#fff" stroke-width="1" width="26" height="16" fill="url(#{{ color }})" rx="3"></rect>
      <text x="4" y="11.5" font-family="Arial" font-size="12" fill="#000">{{ level }}</text>
      <rect x="26" y="5" stroke="#fff" stroke-width="1" width="3" height="6" fill="gray"></rect>
    </g>
</svg>''')
title_bar_style = jinja2.Template('''
QToolBar {
    margin: 0px; 
    border: 0px; 
    color: #fff;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #c24e2b, stop : 0.143 #c7502c, stop : 0.286 #cc522d, stop : 0.429 #d0542e, stop : 0.571 #d55630, stop : 0.714 #da5831, stop : 0.857 #df5a32, stop : 1.0 #e45c33);

    /* background: #000; */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
    /* background: url({{ TITLEBAR_BACKGROUND_URL }}) */
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929); */    
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
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
class BatteryIndicator(QToolButton):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(BatteryIndicator, self).__init__(parent)
        self.level = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        self.battery = battery
        self.backend = Battery()
        self.setFixedSize(QSize(30,30))
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
        }''')
        self.pluggedIcon = QToolButton(self)
        self.pluggedIcon.setStyleSheet('''
        QToolButton {
            border: 0px;
        }''')

    def getColor(self, level):
        if level < 33:
            return "grad3"
        elif level < 66:
            return "grad2"
        else:
            return "grad1"

    def setBattery(self, level: int):
        level = max(min(level, 100), 0)
        color = self.getColor(level)
        svg_bytes = bytes(self.battery.render(
            color=color,
            level=level,
        ), encoding='utf-8')
        self._battery_image = QImage.fromData(svg_bytes)
        self._battery_pixmap = QPixmap.fromImage(self._battery_image)
        self.setIcon(QIcon(self._battery_pixmap))
        self.setIconSize(QSize(30,30))

    def update(self):
        plugged, percent = self.backend()
        if plugged: 
            self.pluggedIcon.setIcon(FigD.Icon("titlebar/plug.svg"))
        else:
            self.pluggedIcon.setIcon(QIcon(None))
        self.setBattery(int(percent))


class FullScreenBtn(QToolButton):
    def __init__(self, parent: Union[QWidget, None]=None, **kwargs):
        super(FullScreenBtn, self).__init__(parent)
        self.setToolTip("toggle fullscreen button")
        self.fs_icon = FigD.Icon(kwargs.get("fs_icon"))
        self.efs_icon = FigD.Icon(kwargs.get("efs_icon"))
        self.is_fullscreen = False
        self.setIcon(self.fs_icon)
        self.setIconSize(QSize(22,22))
        self.clicked.connect(self.toggle)
        self.setStyleSheet(title_btn_style)
        self.titlebar = None

    def connectTitleBar(self, titlebar):
        self.titlebar = titlebar

    def fullscreen(self):
        print("fullscreen mode")        
        self.window().showFullScreen()
        self.setIcon(self.efs_icon)
        self.is_fullscreen = True
        if self.titlebar:
            self.titlebar.showInfo()

    def exit_fullscreen(self):
        print("exiting fullscreen mode")
        self.window().showNormal()
        self.setIcon(self.fs_icon)
        self.is_fullscreen = False
        if self.titlebar:
            self.titlebar.hideInfo()

    def toggle(self):
        if self.is_fullscreen:
            self.exit_fullscreen()
        else: 
            self.fullscreen()


class WifiBtn(QToolButton):
    def __init__(self, parent: Union[QWidget, None]=None, **kwargs):
        super(WifiBtn, self).__init__(parent)
        self.setToolTip("open wifi settings")
        self.setIcon(FigD.Icon("titlebar/wifi_3.svg"))
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
        }''')
        self.network_manager = NetworkHandler().manager
        name = self.network_manager.net_info.name
        self.netName = QLabel(name)
        self.netName.setStyleSheet('''
        QLabel {
            color: #292929;
            font-size: 16px;
            background: transparent;
            padding-left: 0px;
            padding-right: 3px;
        }''')


class VolumeBtn(QToolButton):
    def __init__(self, parent: Union[QWidget, None]=None, default=None):
        super(VolumeBtn, self).__init__(parent)
        self.setStyleSheet("""
        QToolButton {
            border: 0px;
            padding: 0px;
            background: transparent;
        }""")
        self.level = "high"
        self.setIcon(FigD.Icon(f"titlebar/{self.level}.svg"))
        self.setIconSize(QSize(20,20))
    
    def enterEvent(self, event):
        self.setIcon(FigD.Icon(f"titlebar/{self.level}_active.svg"))
        super(VolumeBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(f"titlebar/{self.level}.svg"))
        super(VolumeBtn, self).leaveEvent(event)


class VolumeLabel(QWidget):
    def __init__(self, parent: Union[QWidget, None]=None, default=None):
        super(VolumeLabel, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        # volume change button        
        self.btn = VolumeBtn()
        self.layout.addWidget(self.btn)
        # volume level readout label.
        if default is None:
            self.label = QLabel("100")
        else:
            self.label = QLabel(str(default))
        self.layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setStyleSheet("""
        QLabel {
            color: #292929;
            margin: 0px;
            padding: 0px;
            font-size: 16px;
            background: transparent;
        }""")

    def set(self, value):
        if not isinstance(value, (float, int)): 
            print(f"tried to set value using a {type(value)} argument")
            return
        if value == 0:
            self.btn.setIcon(FigD.Icon("titlebar/mute.svg"))
        elif value < 33:
            self.btn.setIcon(FigD.Icon("titlebar/low.svg"))
        elif value <= 66:
            self.btn.setIcon(FigD.Icon("titlebar/medium.svg"))
        else: 
            self.btn.setIcon(FigD.Icon("titlebar/high.svg"))
        self.label.setText(str(int(value)))

class ZoomSlider(QSlider):
    def __init__(self):
        super(ZoomSlider, self).__init__(Qt.Horizontal)
        self.setFixedWidth(100)
        self.setMaximum(250)
        self.setMinimum(25)
        self.setValue(125)
        # self.valueChanged.connect(self.setTabZoom)
        self.sliderReleased.connect(self.setTabZoom)
        # self.setStyleSheet("color: #292929;")
    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget

    def connectLabel(self, label):
        self.label = label
        self.label.returnPressed.connect(self.setTabZoomFromLabel)

    def setTabZoom(self):
        zoom = self.value()
        self.label.setText(f"{zoom}")
        self.tabWidget.setTabZoom(zoom)

    def setTabZoomFromLabel(self):
        zoom = self.label.text()
        try:
            zoom = int(zoom)
        except ValueError as e:
            print(f"{e} reseting slider, label value to 125")
            zoom = 125
            self.label.setText("125")
        if zoom < 25:
            zoom = 25
            self.label.setText("25")
        elif zoom > 500:
            zoom = 500
            self.label.setText("500")
        self.tabWidget.setTabZoom(zoom)


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
            callback=self.callback if parent is None else parent.hide
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
        # # widget bar toggle button
        # self.widgetsToggleBtn = self.initTitleBtn(
        #     "titlebar/widgets_bar.svg", 
        #     tip="toggle dashboard widgets visibility",
        #     callback=self.callback if parent is None else parent.floatmenu.toggle 
        # )
        self.printBtn = self.initTitleBtn(
            "titlebar/print.svg", 
            tip="print the webpage (as PDF).",
            callback=self.callback if parent is None else parent.tabs.printPage
        ) 
        self.viewSourceBtn = self.initTitleBtn(
            "titlebar/source.svg", 
            tip="view the source of the webpage.",
            callback=self.callback if parent is None else parent.tabs.viewSource
            # callback=self.callback if parent is None else parent.tabs.save
        )
        self.saveSourceBtn = self.initTitleBtn(
            "titlebar/save.svg", 
            tip="save the source of the webpage.",
            callback=self.callback if parent is None else parent.tabs.save
        )
        self.zoomInBtn = self.initTitleBtn(
            "titlebar/zoom_in.svg", 
            tip="zoom in",
            # callback=self.callback if parent is None else parent.tabs.save
        )
        # self.wordCountBtn = self.initTitleBtn(
        #     "titlebar/word_count.svg", 
        #     tip="toggle visibility of word count, time to read display",
        #     callback=self.callback if parent is None else parent.page_info.toggle
        # )
        self.findBtn = self.initTitleBtn(
            "titlebar/find_in_page.svg", 
            tip="find in page",
            # callback=self.callback if parent is None else parent.tabs.save
        )
        self.devToolsBtn = self.initTitleBtn(
            "titlebar/dev_tools.svg", 
            tip="toggle dev tools sidebar.",
            callback=self.callback if parent is None else parent.tabs.toggleDevTools
        )
        self.zoomOutBtn = self.initTitleBtn(
            "titlebar/zoom_out.svg", 
            tip="zoom out",
            # callback=self.callback if parent is None else parent.tabs.save
        )
        self.fullscreenBtn = FullScreenBtn(
            fs_icon="titlebar/fullscreen.svg", 
            efs_icon="titlebar/exit_fullscreen.svg", 
        )
        self.bluetoothBtn = self.initTitleBtn(
            "titlebar/bluetooth.svg", 
            tip="open ubuntu's bluetooth panel.",
            # callback=self.callback if parent is None else parent.tabs.save
        )
        self.bluetoothBtn.setFixedSize(QSize(17,17))
        self.fullscreenBtn.connectTitleBar(self)
        # self.onScreenKeyboard = self.initTitleBtn(
        #     "titlebar/onscreenkeyboard.svg", 
        #     tip="open on screen keyboard.",
        #     # callback=self.callback if parent is None else parent.tabs.save
        # )
        # self.transBtn = self.initTitleBtn(
        #     "titlebar/trans.svg", 
        #     tip="open translation utility.",
        #     # callback=self.callback if parent is None else parent.tabs.save
        # )
        # self.ttsBtn = self.initTitleBtn(
        #     "titlebar/tts.svg", 
        #     tip="open text to speech.",
        #     # callback=self.callback if parent is None else parent.tabs.save
        # )
        self.zoomSlider = ZoomSlider()
        self.zoomLabel = QLineEdit()
        self.zoomLabel.setText("125")
        self.zoomLabel.setStyleSheet("""
        QLineEdit {
            color: #292929; /* #39a4e7; */
            font-size: 16px;
            font-weight: bold;
            background: transparent;
        }""")
        self.zoomSlider.connectLabel(self.zoomLabel)
        palette = QPalette()
        palette.setColor(QPalette.Highlight, QColor(29, 29, 29))
        self.zoomSlider.setPalette(palette)
        # self.zoomSlider.setAutoFillBackground(True)
        self.zoomLabel.setMaximumWidth(35)

        self.wifi = WifiBtn()
        self.wifi.setFixedSize(QSize(18,18))

        self.infoDisplay = QWidget()
        self.infoLayout = QHBoxLayout()
        self.infoLayout.setSpacing(2)
        self.infoLayout.setContentsMargins(0,0,0,0)
        self.infoDisplay.setLayout(self.infoLayout)

        self.volume = VolumeLabel()

        self.battery = BatteryIndicator(self)
        self.battery.setFixedSize(QSize(25,25))
        self.battery.pluggedIcon.setFixedSize(QSize(17,17))
        # window title
        self.title = QLabel()
        self.title.setText("fig-dash: a dashboard for Python developers")
        self.title.setStyleSheet("font-family: 'Be Vietnam Pro', sans-serif; font-weight: bold; color: #fff; font-size: 16px;")
        # self.title.setAlignment(Qt.AlignCenter)
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # lang settings.
        self.langBtn = QToolButton(self)
        self.langBtn.setText("En")
        self.langBtn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 15px;
            font-family: 'Be Vietnam Pro', sans-serif;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 0.5);
            /* background: rgba(255, 223, 97, 0.5); */
        }''')
        self.addWidget(self.closeBtn)
        self.addWidget(self.minimizeBtn)
        self.addWidget(self.maximizeBtn)
        self.addWidget(self.initBlank())
        self.addWidget(self.viewSourceBtn)
        self.addWidget(self.saveSourceBtn)
        self.addWidget(self.devToolsBtn)
        self.addWidget(self.findBtn)
        self.addWidget(self.printBtn)
        self.addWidget(self.zoomOutBtn)
        self.addWidget(self.zoomLabel)
        self.addWidget(self.zoomSlider)
        self.addWidget(self.zoomInBtn)
        self.addWidget(self.initSpacer(30))
        self.addWidget(self.title)
        self.addWidget(self.initSpacer())
        self.infoLayout.addWidget(self.wifi, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.infoLayout.addWidget(self.wifi.netName, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.infoLayout.addWidget(self.volume, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.infoLayout.addWidget(self.langBtn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.infoLayout.addWidget(self.bluetoothBtn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.infoLayout.addWidget(self.battery.pluggedIcon, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.infoLayout.addWidget(self.battery)
        self.addWidget(self.infoDisplay)
        # self.addWidget(self.wifi)
        # self.addWidget(self.wifi.netName)
        # self.addWidget(self.volume)
        # self.addWidget(self.langBtn)
        # self.addWidget(self.bluetoothBtn)
        # self.addWidget(self.battery.pluggedIcon)
        # self.addWidget(self.battery)
        # self.addWidget(self.onScreenKeyboard)
        # self.addWidget(self.transBtn)
        # self.addWidget(self.ttsBtn)
        self.addWidget(self.initBlank())
        self.addWidget(self.fullscreenBtn)
        self.addWidget(self.initBlank())
        self.setMaximumHeight(30)
        self.hideInfo()

    def hideInfo(self):
        # print("\x1b[33;1mhiding info\x1b[0m")
        self.wifi.hide()
        self.wifi.netName.hide()
        self.volume.hide()
        self.langBtn.hide()
        self.bluetoothBtn.hide()
        self.battery.pluggedIcon.hide()
        self.battery.hide()
        self.isInfoVisible = False

    def activate(self):
        self.closeBtn.setIcon(FigD.Icon("titlebar/close.svg"))
        self.maximizeBtn.setIcon(FigD.Icon("titlebar/maximize.svg"))
        self.minimizeBtn.setIcon(FigD.Icon("titlebar/minimize.svg"))

    def deactivate(self):
        icon = "titlebar/disabled.svg"
        self.closeBtn.setIcon(FigD.Icon(icon))
        self.maximizeBtn.setIcon(FigD.Icon(icon))
        self.minimizeBtn.setIcon(FigD.Icon(icon))

    def toggleInfo(self):
        if self.isInfoVisible:
            self.hideInfo()
        else: self.showInfo()

    def showInfo(self):
        # print("\x1b[33;1mshowing info\x1b[0m")
        self.wifi.show()
        self.wifi.netName.show()
        self.volume.show()
        self.langBtn.show()
        self.bluetoothBtn.show()
        self.battery.pluggedIcon.show()
        self.battery.show()
        self.isInfoVisible = True

    def maximize(self):
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            if parent.isMaximized():
                parent.showNormal()
            else:
                parent.showMaximized()

    def initSpacer(self, width=None):
        spacer = QWidget()
        if width:
            spacer.setMinimumWidth(width)
            spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        else:
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        return spacer

    def connectTabWidget(self, tabWidget):
        self.tabs = tabWidget
        self.findBtn.clicked.connect(self.tabs.triggerFind)
        self.zoomInBtn.clicked.connect(self.tabs.zoomInTab)
        self.zoomOutBtn.clicked.connect(self.tabs.zoomOutTab)
        # self.saveSourceBtn.clicked.connect(self.tabs.saveAs)
        self.CtrlS = QShortcut(QKeySequence("Ctrl+S"), self)
        self.CtrlS.activated.connect(self.tabs.saveAs)
        self.zoomSlider.connectTabWidget(self.tabs)

    def initBlank(self):
        btn = QToolButton(self)
        btn.setIcon(QIcon(None))
        btn.setStyleSheet("border: 0px;")
        return btn

    def initTitleBtn(self, icon, **kwargs):
        btn = QToolButton(self)
        btn.setToolTip(kwargs.get("tip", "a tip"))
        btn.setIcon(FigD.Icon(icon))
        size = kwargs.get("size", (22,22))
        btn.setIconSize(QSize(*size))
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
        try:
            delta = QPoint(event.globalPos() - parent.oldPos)
            parent.move(parent.x() + delta.x(), parent.y() + delta.y())
            parent.oldPos = event.globalPos()
        except Exception as e:
            print("\x1b[31;1mtitlebar.mouseMoveEvent\x1b[0m", e)


def titlebar_test():
    app = QApplication(sys.argv)
    window = QMainWindow()
    titlebar = TitleBar(window)
    window.addToolBar(Qt.TopToolBarArea, titlebar)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    titlebar_test()