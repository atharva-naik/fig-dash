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
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer, QStringListModel
from PyQt5.QtWidgets import QSlider, QWidget, QAction, QApplication, QLabel, QLineEdit, QToolBar, QToolButton, QMainWindow, QShortcut, QSizePolicy, QHBoxLayout, QCompleter
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
title_bar_default_bg = """qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #c24e2b, stop : 0.143 #c7502c, stop : 0.286 #cc522d, stop : 0.429 #d0542e, stop : 0.571 #d55630, stop : 0.714 #da5831, stop : 0.857 #df5a32, stop : 1.0 #e45c33)"""
title_bar_style = jinja2.Template('''
QToolBar {
    margin: 0px; 
    border: 0px; 
    color: #fff;
    spacing: 0px;
    background: {{ TITLEBAR_BACKGROUND_COLOR }};
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
    border-radius: 12px; 
    font-family: Helvetica;
}
QToolButton:hover {
    background: rgba(255, 255, 255, 0.5);
    /* background: rgba(255, 223, 97, 0.5); */
}'''
title_btn_style_l = jinja2.Template('''
QToolButton {
    padding: 2px;
    padding-left: 5px;
    background: {{ BACKGROUND }};
    font-family: Helvetica;
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}''')
title_btn_style_c = jinja2.Template('''
QToolButton {
    padding: 2px;
    background: {{ BACKGROUND }};
    font-family: Helvetica;
}''')
title_btn_style_r = jinja2.Template('''
QToolButton {
    padding: 2px;
    padding-right: 5px;
    background: {{ BACKGROUND }};
    font-family: Helvetica;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}''')

window_title_btn_style = '''
QToolButton {
    border-radius: 11px; 
    font-family: Helvetica;
}
QToolButton:hover {
    background: rgba(255, 255, 255, 0.5);
    /* background: rgba(255, 223, 97, 0.5); */
}'''
window_title_bar_style = jinja2.Template('''
QToolBar {
    margin: 0px; 
    border: 0px; 
    color: #fff;
    spacing: 0px;
    /* background: background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
    background: transparent;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
}
''')
class TabSearchBar(QLineEdit):
    """need to connect to QTabWidget, will be added to the TitleBar."""
    def __init__(self, parent: Union[None, QWidget]=None):
        super(TabSearchBar, self).__init__(parent)
        # self.label = QLabel("")
        # self.label.setParent(self)
        # self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        # view site info.
        self.searchAction = QAction()
        self.searchAction.setIcon(FigD.Icon("titlebar/search_tabs.svg"))
        self.addAction(self.searchAction, self.LeadingPosition)
        self.setPlaceholderText("search tabs")
        # set size of tab search bar.
        self.setFixedHeight(26)
        self.setMaximumWidth(300)
        # connections.
        self.returnPressed.connect(self.switchTab)
        # suggestions based on current list of tabs,
        self.completer = QCompleter([])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # set palette for completer.
        palette = self.completer.popup().palette()
        # palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128,128,128))
        palette.setColor(QPalette.Base, QColor(29,29,29))
        palette.setColor(QPalette.Text, QColor(255,255,255))
        palette.setColor(QPalette.Highlight, QColor(235, 95, 52))
        palette.setColor(QPalette.AlternateBase, QColor(29,29,29))
        # palette.setColor(QPalette.Window, QColor(29,29,29,255))
        # palette.setColor(QPalette.WindowText, QColor(255,255,255,255)) 
        self.completer.popup().setPalette(palette)
        # self.completer.popup().setFont()
        self.setCompleter(self.completer)
        # set style sheet.
        self.setStyleSheet("""background: #292929; color: #fff; font-size: 17px; selection-background-color: #eb5f34; border-radius: 7px;""")

    def switchTab(self):
        text = self.text()
        try: 
            i = self.tab_list.index(text)
            self.tabs.setCurrentIndex(i)
        except ValueError as e:
            print(e) 
        
    def focusInEvent(self, event):
        super(TabSearchBar, self).focusInEvent(event)
        self.refreshTabList()
        
    def connectTabWidget(self, tabWidget):
        self.tabs = tabWidget

    def setText(self, text: str):
        super(TabSearchBar, self).setText(text)
        self.setCursorPosition(0)

    def refreshTabList(self):
        self.model = QStringListModel()
        tab_list = []
        for i in range(self.tabs.count()):
            text = self.tabs.tabText(i)
            tab_list.append(text.strip()+f" ({i})")
        # print(tab_list)
        self.tab_list = tab_list
        self.model.setStringList(tab_list)
        self.completer.setModel(self.model)


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
        self.titlebar = None
        style = kwargs.get("style", "c")
        BACKGROUND = kwargs.get("background", "#292929")
        if style == "l": self.setStyleSheet(
            title_btn_style_l.render(BACKGROUND=BACKGROUND)
        )
        elif style == "r": self.setStyleSheet(
            title_btn_style_r.render(BACKGROUND=BACKGROUND)
        )
        elif style == "c": self.setStyleSheet(
            title_btn_style_c.render(BACKGROUND=BACKGROUND)
        )
        else: self.setStyleSheet(title_btn_style)

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
        try: self.tabWidget.setTabZoom(zoom)
        except: print(f"\x1b[31;1mui.titlebar.ZoomSlider.setTabZoom:\x1b[0m 'not connected to tabWidget'")

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
        try: self.tabWidget.setTabZoom(zoom)
        except: print(f"\x1b[31;1mui.titlebar.ZoomSlider.setTabZoomFromLabel:\x1b[0m 'not connected to tabWidget'")


class WindowTitleBar(QToolBar):
    def __init__(self, parent: Union[QWidget, None]=None, background: str="#292929"):
        super(WindowTitleBar, self).__init__("Titlebar", parent)
        self.setStyleSheet(window_title_bar_style.render(
            TITLEBAR_BACKGROUND_URL=FigD.icon("titlebar/texture.png")
        ))
        self.background = background
        self.setIconSize(QSize(20,20))
        self.setMovable(False)
        # close window
        self.closeBtn = self.initTitleBtn(
            "titlebar/close_large.svg", 
            tip="close window",
            callback=self.callback if parent is None else parent.hide
        )
        # minimize window
        self.minimizeBtn = self.initTitleBtn(
            "titlebar/minimize_large.svg", 
            tip="minimize window",
            callback=self.callback if parent is None else parent.showMinimized
        )
        # maximize button
        self.maximizeBtn = self.initTitleBtn(
            "titlebar/maximize_large.svg", 
            tip="maximize window",
            callback=self.maximize
        )
        self.printBtn = self.initTitleBtn(
            "titlebar/print.svg", 
            tip="print the webpage (as PDF).",
            style="c",
            # callback=self.callback if parent is None else parent.tabs.printPage
        ) 
        self.viewSourceBtn = self.initTitleBtn(
            "titlebar/source.svg", style="l",
            tip="view the source of the webpage.",
            # callback=self.callback if parent is None else parent.tabs.viewSource
        )
        self.saveSourceBtn = self.initTitleBtn(
            "titlebar/save.svg", style="c",
            tip="save the source of the webpage.",
            # callback=self.callback if parent is None else parent.tabs.save
        )
        self.zoomInBtn = self.initTitleBtn(
            "titlebar/zoom_in.svg", 
            tip="zoom in", style="r",
        )
        self.findBtn = self.initTitleBtn(
            "titlebar/find_in_page.svg", 
            tip="find in page", style="c",
        )
        self.devToolsBtn = self.initTitleBtn(
            "titlebar/dev_tools.svg", style="c",
            tip="toggle dev tools sidebar.",
            # callback=self.callback if parent is None else parent.tabs.toggleDevTools
        )
        self.zoomOutBtn = self.initTitleBtn(
            "titlebar/zoom_out.svg", 
            tip="zoom out", style="c",
        )
        self.fullscreenBtn = FullScreenBtn(
            fs_icon="titlebar/fullscreen.svg", 
            efs_icon="titlebar/exit_fullscreen.svg", 
            style="r", background=background,
        )
        self.ribbonCollapseBtn = self.initTitleBtn(
            "titlebar/widgets_bar.svg", 
            tip="collapse the ribbon menu",
            style="l",
        )

        self.zoomSlider = ZoomSlider()
        self.zoomLabel = QLineEdit()
        self.zoomLabel.setText("125")
        self.zoomLabel.setStyleSheet("""
        QLineEdit {
            padding: 1px;
            color: #34b4eb; /* #39a4e7; */
            font-size: 16px;
            font-weight: bold;
            background: transparent;
        }""")
        self.zoomSlider.connectLabel(self.zoomLabel)
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(41, 41, 41))
        palette.setColor(QPalette.Highlight, QColor(52, 180, 235))
        self.zoomSlider.setPalette(palette)
        # self.zoomSlider.setAutoFillBackground(True)
        self.zoomLabel.setMaximumWidth(35)

        # window title
        self.title = QLabel()
        # self.title.setText("fig-dash: a dashboard for Python developers")
        self.title.setStyleSheet("font-family: 'Be Vietnam Pro', sans-serif; font-weight: bold; color: #fff; font-size: 16px;")
        # self.title.setAlignment(Qt.AlignCenter)
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # to display window icon.
        self.windowIcon = QLabel()

        self.addWidget(self.initBlank(5))
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
        self.addWidget(self.ribbonCollapseBtn)
        self.addWidget(self.fullscreenBtn)
        self.addWidget(self.initBlank())
        self.addWidget(self.windowIcon)
        self.addWidget(self.initBlank(5))
        self.setMaximumHeight(30)

    def setWindowIcon(self, winIcon):
        self.windowIcon.setPixmap(
            winIcon.pixmap(QSize(30,30))
        )

    def activate(self):
        self.closeBtn.setIcon(FigD.Icon("titlebar/close.svg"))
        self.maximizeBtn.setIcon(FigD.Icon("titlebar/maximize.svg"))
        self.minimizeBtn.setIcon(FigD.Icon("titlebar/minimize.svg"))

    def deactivate(self):
        icon = "titlebar/disabled.svg"
        self.closeBtn.setIcon(FigD.Icon(icon))
        self.maximizeBtn.setIcon(FigD.Icon(icon))
        self.minimizeBtn.setIcon(FigD.Icon(icon))

    def maximize(self):
        parent = self.window
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

    def connectWindow(self, window):
        self.window = window
        self.closeBtn.clicked.connect(window.close)
        self.minimizeBtn.clicked.connect(window.showMinimized)
        # self.findBtn.clicked.connect(self.tabs.triggerFind)
        # self.zoomInBtn.clicked.connect(self.tabs.zoomInTab)
        # self.zoomOutBtn.clicked.connect(self.tabs.zoomOutTab)
        # self.saveSourceBtn.clicked.connect(self.tabs.saveAs)
        # self.CtrlS = QShortcut(QKeySequence("Ctrl+S"), self)
        # self.CtrlS.activated.connect(self.tabs.saveAs)
        # self.zoomSlider.connectTabWidget(self.tabs)
    def initBlank(self, width: Union[None, int]=None):
        btn = QToolButton(self)
        btn.setIcon(QIcon(None))
        btn.setStyleSheet("border: 0px;")
        if width is not None:
            btn.setFixedWidth(width)

        return btn

    def initTitleBtn(self, icon, **kwargs):
        btn = QToolButton(self)
        btn.setToolTip(kwargs.get("tip", "a tip"))
        btn.setIcon(FigD.Icon(icon))
        size = kwargs.get("size", (22,22))
        btn.setIconSize(QSize(*size))
        btn.clicked.connect(kwargs.get("callback", self.callback))
        style = kwargs.get("style", "default")
        BACKGROUND = self.background
        if style == "l": btn.setStyleSheet(
            title_btn_style_l.render(BACKGROUND=BACKGROUND)
        )
        elif style == "r": btn.setStyleSheet(
            title_btn_style_r.render(BACKGROUND=BACKGROUND)
        )
        elif style == "c": btn.setStyleSheet(
            title_btn_style_c.render(BACKGROUND=BACKGROUND)
        )
        else: btn.setStyleSheet(window_title_btn_style)

        return btn

    def callback(self):
        pass

    def mousePressEvent(self, event):
        parent = self.window
        if parent is None: return
        parent.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        parent = self.window
        if parent is None: return
        try:
            delta = QPoint(event.globalPos() - parent.oldPos)
            parent.move(parent.x() + delta.x(), parent.y() + delta.y())
            parent.oldPos = event.globalPos()
        except Exception as e:
            pass
            # print("\x1b[31;1mtitlebar.mouseMoveEvent\x1b[0m", e)

class TitleBar(QToolBar):
    def __init__(self, parent: Union[QWidget, None]=None, background: str="#292929"):
        super(TitleBar, self).__init__("Titlebar", parent)
        self.background = background
        self.setStyleSheet(title_bar_style.render(
            TITLEBAR_BACKGROUND_URL=FigD.icon("titlebar/texture.png"),
            TITLEBAR_BACKGROUND_COLOR=title_bar_default_bg,
        ))
        self.tab_searchbar = TabSearchBar()
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
            "titlebar/print.svg", style="c",
            tip="print the webpage (as PDF).",
            size=(18,18),
            # callback=self.callback if parent is None else parent.tabs.printPage
        ) 
        self.viewSourceBtn = self.initTitleBtn(
            "titlebar/source.svg", style="l",
            tip="view the source of the webpage.",
            size=(18,18),
            # callback=self.callback if parent is None else parent.tabs.viewSource
        )
        self.saveSourceBtn = self.initTitleBtn(
            "titlebar/save.svg", style="c",
            tip="save the source of the webpage.",
            size=(18,18),
            # callback=self.callback if parent is None else parent.tabs.save
        )
        self.zoomInBtn = self.initTitleBtn(
            "titlebar/zoom_in.svg", 
            tip="zoom in", style="r",
            size=(18,18),
        )
        self.accountBtn = self.initTitleBtn(
            "navbar/account.png",
            tip="open account settings",
            # style=dash_bar_btn_style,
            # size=(24,24)
        )
        # self.wordCountBtn = self.initTitleBtn(
        #     "titlebar/word_count.svg", 
        #     tip="toggle visibility of word count, time to read display",
        #     callback=self.callback if parent is None else parent.page_info.toggle
        # )
        self.findBtn = self.initTitleBtn(
            "titlebar/find_in_page.svg", 
            tip="find in page", style="c",
            size=(18,18),
        )
        self.devToolsBtn = self.initTitleBtn(
            "titlebar/dev_tools.svg", style="c",
            tip="toggle dev tools sidebar.",
            size=(18,18),
            # callback=self.callback if parent is None else parent.tabs.toggleDevTools
        )
        self.zoomOutBtn = self.initTitleBtn(
            "titlebar/zoom_out.svg", 
            tip="zoom out", style="c",
            size=(18,18),
        )
        self.fullscreenBtn = FullScreenBtn(
            fs_icon="titlebar/fullscreen.svg", 
            efs_icon="titlebar/exit_fullscreen.svg", 
        )
        self.bluetoothBtn = self.initTitleBtn(
            "titlebar/bluetooth.svg", 
            tip="open ubuntu's bluetooth panel.",
        )
        self.bluetoothBtn.setFixedSize(QSize(17,17))
        self.fullscreenBtn.connectTitleBar(self)
        # self.onScreenKeyboard = self.initTitleBtn(
        #     "titlebar/onscreenkeyboard.svg", 
        #     tip="open on screen keyboard.",
        # )
        # self.transBtn = self.initTitleBtn(
        #     "titlebar/trans.svg", 
        #     tip="open translation utility.",
        # )
        # self.ttsBtn = self.initTitleBtn(
        #     "titlebar/tts.svg", 
        #     tip="open text to speech.",
        # )
        self.zoomSlider = ZoomSlider()
        self.zoomLabel = QLineEdit()
        self.zoomLabel.setText("125")
        self.zoomLabel.setStyleSheet("""
        QLineEdit {
            color: #fff; /* #39a4e7; */
            background: #292929;
            font-size: 16px;
            font-weight: bold;
        }""")
        self.zoomSlider.connectLabel(self.zoomLabel)
        palette = QPalette()
        palette.setColor(QPalette.Highlight, QColor(52, 180, 235))
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
        # self.title.setText("fig-dash: a dashboard for Python developers")
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
        self.addWidget(self.tab_searchbar)
        self.addWidget(self.initBlank2(5))
        self.addWidget(self.accountBtn)
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

    def setTitleBarColor(self, r: int, g: int, b: int):
        self.setStyleSheet(title_bar_style.render(
            TITLEBAR_BACKGROUND_COLOR=f"rgb({r},{g},{b})",
        ))

    def connectTabWidget(self, tabWidget):
        self.tabs = tabWidget
        self.findBtn.clicked.connect(self.tabs.triggerFind)
        self.zoomInBtn.clicked.connect(self.tabs.zoomInTab)
        self.zoomOutBtn.clicked.connect(self.tabs.zoomOutTab)
        
        self.printBtn.clicked.connect(self.tabs.printPage) 
        self.viewSourceBtn.clicked.connect(self.tabs.viewSource)
        self.saveSourceBtn.clicked.connect(self.tabs.save)
        self.devToolsBtn.clicked.connect(self.tabs.toggleDevTools)

        # self.saveSourceBtn.clicked.connect(self.tabs.saveAs)
        self.CtrlS = QShortcut(QKeySequence("Ctrl+S"), self)
        self.CtrlS.activated.connect(self.tabs.saveAs)
        self.zoomSlider.connectTabWidget(self.tabs)
        self.tab_searchbar.connectTabWidget(self.tabs)

    def initBlank2(self, width=10):
        btn = QWidget()
        btn.setFixedWidth(width)
        btn.setStyleSheet("border 0px; background: transparent;")

        return btn

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
        style = kwargs.get("style", "default")
        BACKGROUND = self.background
        if style == "l": btn.setStyleSheet(
            title_btn_style_l.render(BACKGROUND=BACKGROUND)
        )
        elif style == "r": btn.setStyleSheet(
            title_btn_style_r.render(BACKGROUND=BACKGROUND)
        )
        elif style == "c": btn.setStyleSheet(
            title_btn_style_c.render(BACKGROUND=BACKGROUND)
        )
        else: btn.setStyleSheet(title_btn_style)

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