#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::titlebar")
# titlebar for the main window
import sys
import jinja2
from typing import *
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.widget.boolean_toggle import AnimatedToggle
# PyQt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QKeySequence, QColor, QPalette, QPainter
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer, QStringListModel
from PyQt5.QtWidgets import QSlider, QWidget, QMenu, QAction, QApplication, QLabel, QLineEdit, QToolBar, QToolButton, QMainWindow, QShortcut, QSizePolicy, QHBoxLayout, QCompleter, QVBoxLayout, QScrollArea
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
}'''
title_btn_style_l = jinja2.Template('''
QToolButton {
    padding: 2px;
    padding-left: 5px;
    background: {{ BACKGROUND }};
    font-size: 15px;
    font-family: Helvetica;
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}''')
title_btn_style_c = jinja2.Template('''
QToolButton {
    border: 0px;
    padding: 2px;
    font-size: 15px;
    background: {{ BACKGROUND }};
    font-family: Helvetica;
}''')
title_btn_style_r = jinja2.Template('''
QToolButton {
    padding: 2px;
    font-size: 15px;
    padding-right: 5px;
    font-family: Helvetica;
    background: {{ BACKGROUND }};
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}''')

window_title_ctrl_btn_style = '''
QToolButton {
    border-radius: 11px; 
    font-family: Helvetica;
}'''
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
def extractSliderColor(bg, where="back"):
    if ("qlineargradient" in bg or "qconicalgradient" in bg) and (where=="back"):
        sliderColor = bg.split(":")[-1].strip()
        sliderColor = sliderColor.split()[-1]
        sliderColor = sliderColor.split(")")[0]
        sliderColor = sliderColor.strip()
    elif ("qlineargradient" in bg or "qconicalgradient" in bg) and (where=="front"):
        sliderColor = bg.split("stop")[1]
        sliderColor = sliderColor.split("#")[-1]
        sliderColor = sliderColor.split(",")[0]
        sliderColor = "#"+sliderColor.strip()
    else: 
        sliderColor = "white" 

    return sliderColor

def styleContextMenu(menu, accent_color: str="yellow"):
    menu.setAttribute(Qt.WA_TranslucentBackground)
    menu.setObjectName("FigDMenu")
    menu.setStyleSheet(jinja2.Template("""
    QMenu#FigDMenu {
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
    	color: #fff;
    	padding: 10px;
    	border-radius: 15px;
    }
    QMenu#FigDMenu::item:selected {
    	color: #292929; 
        border-radius: 5px;
    	background-color: {{ ACCENT_COLOR }}; 
    }
    QMenu#FigDMenu:separator {
    	background: #292929;
    }""").render(ACCENT_COLOR=accent_color))
    palette = menu.palette()
    palette.setColor(QPalette.Base, QColor(48,48,48))
    palette.setColor(QPalette.Text, QColor(125,125,125))
    palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    # palette.setColor(QPalette.PlaceholderText, QColor(125,125,125))
    palette.setColor(QPalette.Window, QColor(255,255,255))
    palette.setColor(QPalette.Highlight, QColor(235,95,52))
    menu.setPalette(palette)

    return menu

def resize_text(text, length=10):
    return (text+" "*(length-len(text)))[:length]

def rotate_text(text, step=0):
    return text[-step:]+text[:-step]

class TitleBarAnimatedLabel(QLabel):
    def __init__(self, parent: Union[QWidget, None]=None):
        """Animated title bar widget
        Args:
            text (str): initial text for animated title bar
            timing (int, optional): time interval of every update. Defaults to 100.
            parent (Union[QWidget, None], optional): parent of QLabel. Defaults to None.
        """
        super(TitleBarAnimatedLabel, self).__init__(parent)
        self.MAX = 24
        self.step_ctr = 0
        self.timing = 200
        self.raw_text = ""
        self.init_text = resize_text(self.raw_text, self.MAX)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(
            self.shiftTitle
        )
        # self.animation_timer.start(timing)
        # self.setText(self.init_text)
    def setAnimatedText(self, text: str, timing: int=200):
        self.init_text = resize_text(text, self.MAX)
        self.timing = timing
        self.raw_text = text
        self.animation_timer.stop()
        self.animation_timer.start(timing)

    def setText(self, text: str):
        self.setAlignment(Qt.AlignCenter)
        super(TitleBarAnimatedLabel, self).setText(text)

    def resizeEvent(self, event):
        # print("width =", self.width())
        # self.animation_timer.stop()
        # self.animation_timer.start(self.timing)
        self.step_ctr = 0
        self.MAX = int(self.width()*24/218)
        self.init_text = resize_text(self.raw_text, self.MAX)
        super(TitleBarAnimatedLabel, self).resizeEvent(event)

    def shiftTitle(self):
        self.step_ctr = (self.step_ctr+1)%self.MAX
        self.setText(rotate_text(
            self.init_text,
            self.step_ctr
        ))


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
        from fig_dash.api.system.battery import Battery
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


class TitleBarCloseBtn(QToolButton):
    def __init__(self, callback=None, 
                 size: Tuple[int,int]=(22,22)):
        super(TitleBarCloseBtn, self).__init__()
        self.setToolTip("close window")
        self.setIcon(FigD.Icon(
            "titlebar/close_large.svg"
        ))
        self.isDisabled = False
        self.setIconSize(QSize(*size))
        self.setStyleSheet(window_title_ctrl_btn_style)
        if callback is not None:
            self.clicked.connect(callback)
        self.menu = QMenu()
        self.menu.addAction("Hide")
        self.menu.addAction("Close All")
        accent_color = """qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #a00055, stop : 0.091 #a70054, stop : 0.182 #ae0052, stop : 0.273 #b50250, stop : 0.364 #bc064e, stop : 0.455 #c20b4c, stop : 0.545 #c81149, stop : 0.636 #ce1746, stop : 0.727 #d41e43, stop : 0.818 #d92440, stop : 0.909 #de2a3c, stop : 1.0 #e33138)"""
        self.menu = styleContextMenu(self.menu, accent_color)

    def enterEvent(self, event):
        if not self.isDisabled:
            self.setIcon(FigD.Icon("titlebar/close_large_hover.svg"))
        super(TitleBarCloseBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        if not self.isDisabled:
            self.setIcon(FigD.Icon("titlebar/close_large.svg"))
        super(TitleBarCloseBtn, self).leaveEvent(event)

    def contextMenuEvent(self, event):
        self.menu.popup(event.globalPos())


class TitleBarShortcutsBtn(QToolButton):
    def __init__(self, titlebar=None,
                 size: Tuple[int,int]=(22,22)):
        super(TitleBarShortcutsBtn, self).__init__()
        self.setToolTip("show window shortcuts")
        self.setIcon(FigD.Icon(
            "titlebar/shortcuts.png"
        ))
        self.titlebar = titlebar
        self.setIconSize(QSize(*size))
        self.setStyleSheet(window_title_btn_style)

    def contextMenuEvent(self, event):
        pos = event.globalPos()
        x, y = pos.x(), pos.y()
        window =  self.titlebar.window
        window.shortcuts_pane = window.createShortcutsPane()
        window.shortcuts_pane.move(x, y)
        window.shortcuts_pane.show()
        # print(window.printShortcuts())
        # self.menu.popup(event.globalPos())

class TitleBarMinimizeBtn(QToolButton):
    def __init__(self, callback=None, 
                 size: Tuple[int,int]=(22,22)):
        super(TitleBarMinimizeBtn, self).__init__()
        self.setToolTip("minimize window")
        self.setIcon(FigD.Icon(
            "titlebar/minimize_large.svg"
        ))
        self.isDisabled = False
        self.setIconSize(QSize(*size))
        self.setStyleSheet(window_title_ctrl_btn_style)
        if callback is not None:
            self.clicked.connect(callback)
        self.menu = QMenu()
        self.menu.addAction("Minimize")
        accent_color = """qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #be9433, stop : 0.091 #c49935, stop : 0.182 #ca9d36, stop : 0.273 #cfa238, stop : 0.364 #d5a639, stop : 0.455 #dbab3b, stop : 0.545 #e1af3d, stop : 0.636 #e7b43e, stop : 0.727 #edb940, stop : 0.818 #f3be42, stop : 0.909 #f9c243, stop : 1.0 #ffc745)"""
        self.menu = styleContextMenu(self.menu, accent_color)

    def enterEvent(self, event):
        if not self.isDisabled:
            self.setIcon(FigD.Icon("titlebar/minimize_large_hover.svg"))
        super(TitleBarMinimizeBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        if not self.isDisabled:
            self.setIcon(FigD.Icon("titlebar/minimize_large.svg"))
        super(TitleBarMinimizeBtn, self).leaveEvent(event)

    def contextMenuEvent(self, event):
        self.menu.popup(event.globalPos())


class TitleBarMaximizeBtn(QToolButton):
    def __init__(self, callback=None, 
                 size: Tuple[int,int]=(22,22)):
        super(TitleBarMaximizeBtn, self).__init__()
        self.setToolTip("maximize window")
        self.setIcon(FigD.Icon(
            "titlebar/maximize_large.svg"
        ))
        self.isDisabled = False
        self.setIconSize(QSize(*size))
        self.setStyleSheet(window_title_ctrl_btn_style)
        if callback is not None:
            self.clicked.connect(callback)
        self.menu = QMenu()
        self.menu.addAction("Split View Vertical")
        self.menu.addAction("Split View Horizontal")
        self.menu.addAction(FigD.Icon("titlebar/fullscreen.svg"), "Show Full Screen")
        self.menu.addAction(FigD.Icon("titlebar/exit_fullscreen.svg"), "Exit Full Screen")
        accent_color = """qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #005822, stop : 0.091 #006226, stop : 0.182 #006b2a, stop : 0.273 #00752e, stop : 0.364 #008032, stop : 0.455 #008a36, stop : 0.545 #00943a, stop : 0.636 #009f3e, stop : 0.727 #00a942, stop : 0.818 #00b446, stop : 0.909 #00bf4a, stop : 1.0 #00ca4e)"""
        self.fullscreen = self.menu.actions()[2]
        self.exit_fullscreen = self.menu.actions()[3]
        self.menu = styleContextMenu(self.menu, accent_color)

    def enterEvent(self, event):
        if not self.isDisabled:
            self.setIcon(FigD.Icon("titlebar/maximize_large_hover.svg"))
        super(TitleBarMaximizeBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        if not self.isDisabled:
            self.setIcon(FigD.Icon("titlebar/maximize_large.svg"))
        super(TitleBarMaximizeBtn, self).leaveEvent(event)

    def contextMenuEvent(self, event):
        self.menu.popup(event.globalPos())


class TitleBarRibbonCollapseBtn(QToolButton):
    def __init__(self, callback=None, 
                 size: Tuple[int,int]=(22,22), 
                 accent_color: str="yellow"):
        super(TitleBarRibbonCollapseBtn, self).__init__()
        self.setToolTip("collapse the ribbon menu")
        self.setIcon(FigD.Icon(
            "titlebar/widgets_bar.svg"
        ))
        self.setIconSize(QSize(*size))
        self.setStyleSheet(
            title_btn_style_l.render(
                BACKGROUND=accent_color
        ))
        if callback is not None:
            self.clicked.connect(callback)
        self.menu = QMenu()
        self.menu.addAction(
            FigD.Icon("titlebar/hide.svg"),
            "Hide menu",
        )
        self.menu.addAction(
            FigD.Icon("titlebar/widgets_bar.svg"), 
            "Show simplified\nribbon"
        )
        self.hidemenu = self.menu.actions()[0]
        self.simplify = self.menu.actions()[1]
        self.menu = styleContextMenu(self.menu, accent_color)

    def enterEvent(self, event):
        # self.setIcon(FigD.Icon("titlebar/maximize_large_hover.svg"))
        super(TitleBarRibbonCollapseBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        # self.setIcon(FigD.Icon("titlebar/maximize_large.svg"))
        super(TitleBarRibbonCollapseBtn, self).leaveEvent(event)

    def contextMenuEvent(self, event):
        self.menu.popup(event.globalPos())


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
        from fig_dash.api.system.network import NetworkHandler
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
    def __init__(self, parent: Union[QWidget, None]=None, 
                 background: str="#292929", title_widget=None, 
                 callbacks: dict={}, where: str="back"):
        super(WindowTitleBar, self).__init__("Titlebar", parent)
        self.setStyleSheet(window_title_bar_style.render(
            TITLEBAR_BACKGROUND_URL=FigD.icon("titlebar/texture.png")
        ))
        print(f"\x1b[33;1mwhere:\x1b[0m {where}")
        self.background = background
        self.callbacks = callbacks
        # set icon size and movability.
        self.setIconSize(QSize(20,20))
        self.setMovable(False)
        # close window
        self.closeBtn = TitleBarCloseBtn(
            callback=self.callback if parent is None else parent.hide
        )
        # minimize window
        self.minimizeBtn = TitleBarMinimizeBtn(
            callback=self.callback if parent is None else parent.showMinimized
        )
        # maximize button
        self.maximizeBtn = TitleBarMaximizeBtn(callback=self.maximize)
        self.printBtn = self.initTitleBtn(
            "titlebar/print.svg", 
            tip="print the webpage (as PDF).",
            style="c",
            # callback=self.callback if parent is None else parent.tabs.printPage
        ) 
        if "printBtn" not in callbacks:
            self.printBtn.hide()
        self.viewSourceBtn = self.initTitleBtn(
            "titlebar/source.svg", style="l",
            tip="view the source of the webpage.",
            callback=callbacks.get("viewSourceBtn"),
        )
        if "viewSourceBtn" not in callbacks:
            self.viewSourceBtn.hide()
        self.saveSourceBtn = self.initTitleBtn(
            "titlebar/save.svg", style="c",
            tip="save the source of the webpage.",
            # callback=self.callback if parent is None else parent.tabs.save
        )
        if "saveSourceBtn" not in callbacks:
            self.saveSourceBtn.hide()
        self.zoomInBtn = self.initTitleBtn(
            "titlebar/zoom_in.svg", 
            tip="zoom in", style="r",
        )
        self.findBtn = self.initTitleBtn(
            "titlebar/find_in_page.svg", 
            tip="find in page", style="c",
        )
        if "findBtn" not in callbacks: 
            self.findBtn.hide()
        self.devToolsBtn = self.initTitleBtn(
            "titlebar/dev_tools.svg", style="c",
            tip="toggle dev tools sidebar.",
            # callback=self.callback if parent is None else parent.tabs.toggleDevTools
        )
        if "devToolsBtn" not in callbacks: 
            self.devToolsBtn.hide()
        self.zoomOutBtn = self.initTitleBtn(
            "titlebar/zoom_out.svg", 
            tip="zoom out", 
            style="l" if callbacks=={} else "c",
        )
        self.fullscreenBtn = FullScreenBtn(
            fs_icon="titlebar/fullscreen.svg", 
            efs_icon="titlebar/exit_fullscreen.svg", 
            style="r", background=background,
        )
        self.ribbonCollapseBtn = TitleBarRibbonCollapseBtn(
            callback=callbacks.get("ribbonCollapseBtn"),
            accent_color=background,
        )
        self.accentColorBtn = self.initTitleBtn(
            "titlebar/accent_color.png",
            tip="pick a new accent color",
        )
        self.settingsBtn = self.initTitleBtn(
            "titlebar/settings.svg",
            tip="open window settings",
        )
        self.shortcutsBtn = TitleBarShortcutsBtn(titlebar=self)
        # zoom slider
        self.zoomSlider = ZoomSlider()
        # wrapper for maintaining background color.
        zoomSliderWrapper = QWidget()
        # zoomSliderWrapper.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        zoomSliderWrapper.setFixedHeight(27)
        zoomSliderWrapper.setFixedWidth(100)
        zoomSliderWrapper.setObjectName("ZoomSliderWrapper")
        zoomSliderLayout = QVBoxLayout()
        zoomSliderLayout.setSpacing(0)
        zoomSliderLayout.setContentsMargins(0, 0, 0, 0)
        zoomSliderWrapper.setStyleSheet(jinja2.Template("""
        QWidget#ZoomSliderWrapper {
            background: {{ BACKGROUND }};
        }""").render(BACKGROUND=background))
        zoomSliderLayout.addWidget(self.zoomSlider)
        zoomSliderWrapper.setLayout(zoomSliderLayout)

        self.zoomLabel = QLineEdit()
        self.zoomLabel.setText("125")
        self.zoomLabel.setFixedHeight(27)
        self.zoomLabel.setStyleSheet(jinja2.Template("""
        QLineEdit {
            color: #fff; 
            border: 0px;
            padding: 1px;
            font-size: 16px;
            font-weight: bold;
            background: {{ BACKGROUND }};
            /* #34b4eb; #39a4e7; */
        }""").render(BACKGROUND=background))
        sliderHandleColor = extractSliderColor(self.background, where=where)
        self.zoomSlider.connectLabel(self.zoomLabel)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 0))
        palette.setColor(QPalette.Button, QColor(sliderHandleColor))
        palette.setColor(QPalette.Highlight, QColor(255, 255, 255))
        self.zoomSlider.setPalette(palette)
        # self.zoomSlider.setAutoFillBackground(True)
        self.zoomLabel.setMaximumWidth(35)
        # auto save toggle button.
        self.sliderHandleColor = sliderHandleColor
        self.autoSaveToggle = AnimatedToggle(
            checked_color=sliderHandleColor,
            pulse_checked_color=sliderHandleColor,
        )
        self.autoSaveToggle.setFixedWidth(50)
        self.autoSaveToggle.setFixedHeight(32)
        self.autoSaveToggle.setContentsMargins(0, 0, 12, 0)
        # auto save toggle blank.
        self.autoSaveBlank = self.initBlank(10)
        # auto save toggle icon.
        self.autoSaveIcon = QToolButton()
        self.autoSaveIcon.setText(" Autosave")
        self.autoSaveIcon.setToolTip("Auto save changes to currently opened file")
        self.autoSaveIcon.setStatusTip("Auto save changes to currently opened file")
        self.autoSaveIcon.setIcon(FigD.Icon("widget/weather/save.svg"))
        self.autoSaveIcon.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.autoSaveIcon.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 15px;
            font-family: "Be Vietnam Pro";
            background: transparent;
        }""")
        if "autoSave" not in callbacks:
            self.autoSaveIcon.hide()
            self.autoSaveToggle.hide()
        else:
            self.autoSaveToggle.stateChanged.connect(self.toggleAutoSaveIcon)
        # to display window icon.
        self.windowIcon = QLabel()
        self.title_widget = title_widget
        if title_widget is None:
            self.title = self.initSpacer(text="PlaceholderText()")
        else:
            self.title = QScrollArea()
            self.title.setStyleSheet("""background-color: transparent;""")
            self.title.setWidgetResizable(True)
            self.title.setWidget(self.title_widget)
            self.title.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.title.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # print("\x1b[34;1mtitle_widget:\x1b[0m", title_widget)
        self.addWidget(self.initBlank(10))
        self.addWidget(self.closeBtn)
        self.addWidget(self.initBlank(3))
        self.addWidget(self.minimizeBtn)
        self.addWidget(self.initBlank(3))
        self.addWidget(self.maximizeBtn)
        self.addWidget(self.autoSaveBlank)
        self.addWidget(self.autoSaveIcon)
        self.addWidget(self.autoSaveToggle)
        self.addWidget(self.viewSourceBtn)
        self.addWidget(self.saveSourceBtn)
        self.addWidget(self.devToolsBtn)
        self.addWidget(self.findBtn)
        self.addWidget(self.printBtn)
        self.addWidget(self.zoomOutBtn)
        self.addWidget(self.zoomLabel)
        self.addWidget(zoomSliderWrapper)
        self.addWidget(self.zoomInBtn)
        self.addWidget(self.initBlank(10))
        self.addWidget(self.accentColorBtn)
        self.addWidget(self.initBlank(10))
        self.addWidget(self.shortcutsBtn)
        self.addWidget(self.initBlank(10))
        self.addWidget(self.title)
        self.addWidget(self.initBlank(10))
        self.addWidget(self.settingsBtn)
        self.addWidget(self.initBlank(10))
        self.addWidget(self.ribbonCollapseBtn)
        self.addWidget(self.fullscreenBtn)
        self.addWidget(self.initBlank())
        self.addWidget(self.windowIcon)
        self.addWidget(self.initBlank(10))
        self.setMaximumHeight(30)

    def toggleAutoSaveIcon(self, state: int):
        """toggle the auto save icon color disabled: white, enabled: accent_color"""
        if state == 2:
            # print("self.autoSaveIcon", self.background)
            iconTemplate = jinja2.Template(r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" class="svg_3aeb045a" focusable="false"><path d="M1792 128q27 0 50 10t40 27 28 41 10 50v1664H357l-229-230V256q0-27 10-50t27-40 41-28 50-10h1536zM512 896h1024V256H512v640zm768 512H640v384h128v-256h128v256h384v-384zm512-1152h-128v768H384V256H256v1381l154 155h102v-512h896v512h384V256z" fill="{{ BACKGROUND_COLOR }}"></path></svg>""") 
            iconPath = FigD.createTempPath(iconTemplate.render(BACKGROUND_COLOR=self.sliderHandleColor))
            self.autoSaveIcon.setIcon(QIcon(iconPath))
            self.autoSaveIcon.setStyleSheet("""
            QToolButton {
                color: """+self.sliderHandleColor+""";
                border: 0px;
                font-size: 15px;
                font-family: "Be Vietnam Pro";
                background: transparent;
            }""")
        elif state == 0:
            self.autoSaveIcon.setIcon(FigD.Icon("widget/weather/save.svg"))
            self.autoSaveIcon.setStyleSheet("""
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 15px;
                font-family: "Be Vietnam Pro";
                background: transparent;
            }""")
        self.callbacks["autoSave"]

    def setAnimatedTitle(self, title: str, timing: int=100):
        if self.title_widget is None:
            self.title.setAnimatedText(title, timing=timing)

    def setTitle(self, title: str):
        if self.title_widget is None:
            self.title.setText(title)

    def setWindowIcon(self, winIcon: QIcon, 
                      size: Tuple[int,int]=(30,30)):
        self.windowIcon.setPixmap(
            winIcon.pixmap(QSize(*size))
        )

    def activate(self):
        self.closeBtn.setIcon(FigD.Icon("titlebar/close_large.svg"))
        self.maximizeBtn.setIcon(FigD.Icon("titlebar/maximize_large.svg"))
        self.minimizeBtn.setIcon(FigD.Icon("titlebar/minimize_large.svg"))
        self.closeBtn.isDisabled = False
        self.maximizeBtn.isDisabled = False
        self.minimizeBtn.isDisabled = False

    def deactivate(self):
        icon = "titlebar/disabled_large.svg"
        self.closeBtn.setIcon(FigD.Icon(icon))
        self.maximizeBtn.setIcon(FigD.Icon(icon))
        self.minimizeBtn.setIcon(FigD.Icon(icon))
        self.closeBtn.isDisabled = True
        self.maximizeBtn.isDisabled = True 
        self.minimizeBtn.isDisabled = True

    def maximize(self):
        parent = self.window
        if isinstance(parent, QMainWindow):
            if parent.isMaximized():
                parent.showNormal()
            else:
                parent.showMaximized()

    def initSpacer(self, width=None, text: str=""):
        spacer = TitleBarAnimatedLabel(text)
        spacer.setText(text)
        spacer.setStyleSheet("""
        QLabel {
            color: #eee;
            font-size: 17px;
            border-radius: 7px;
            background: transparent;
            font-family: 'Be Vietnam Pro';
        }""")
        spacer.setFixedHeight(27)
        # spacer.setAlignment(Qt.AlignCenter)
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
        for action in self.closeBtn.menu.actions():
            if action.text() == "Hide":
                action.triggered.connect(window.hide)
        try:
            self.window_name = self.window.appName
        except Exception as e:
            snippet = "self.window_name = self.window.appName"
            print(f"ui::titlebar::WindowTitleBar.connectWindow: {snippet}", e)
        # try: 
        #     self.shortcutsBtn.clicked.connect(self.window.showShortcutList)
        # except Exception as e:
        #     snippet = "self.shortcutsBtn.clicked.connect(self.window.showShortcutList)"
        #     print(f"ui::titlebar::WindowTitleBar.connectWindow: {snippet}", e)

        # self.findBtn.clicked.connect(self.tabs.triggerFind)
        # self.zoomInBtn.clicked.connect(self.tabs.zoomInTab)
        # self.zoomOutBtn.clicked.connect(self.tabs.zoomOutTab)
        # self.saveSourceBtn.clicked.connect(self.tabs.saveAs)
        # self.CtrlS = QShortcut(QKeySequence("Ctrl+S"), self)
        # self.CtrlS.activated.connect(self.tabs.saveAs)
        # self.zoomSlider.connectTabWidget(self.tabs)
    def __str__(self):
        return self.window_name

    def initBlank(self, width: Union[None, int]=None):
        btn = QToolButton(self)
        btn.setIcon(QIcon(None))
        btn.setStyleSheet("border: 0px;")
        if width is not None:
            btn.setFixedWidth(width)

        return btn

    def initTitleBtn(self, icon=None, text=None, **kwargs):
        btn = QToolButton(self)
        btn.setToolTip(kwargs.get("tip", "a tip"))
        if icon: btn.setIcon(FigD.Icon(icon))
        if text: btn.setText(text)
        size = kwargs.get("size", (22,22))
        btn.setIconSize(QSize(*size))
        callback = kwargs.get(
            "callback", 
            self.callback
        )
        btn.clicked.connect(
            self.callback if callback is None else callback
        )
        style = kwargs.get("style", "default")
        BACKGROUND = kwargs.get(
            "background", 
            self.background
        )
        if style == "l": btn.setStyleSheet(
            title_btn_style_l.render(BACKGROUND=BACKGROUND)
        )
        elif style == "r": btn.setStyleSheet(
            title_btn_style_r.render(BACKGROUND=BACKGROUND)
        )
        elif style == "c": btn.setStyleSheet(
            title_btn_style_c.render(BACKGROUND=BACKGROUND)
        )
        else:
            # print("using default style") 
            btn.setStyleSheet(window_title_btn_style)

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
        self.title.setStyleSheet("""
        color: #fff; 
        font-family: 'Be Vietnam Pro', sans-serif; 
        font-weight: bold;
        font-size: 16px;""")
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
    # def define(self, btn: str, callback) -> bool:
    #     """connect `callback` to a `button` (string name) attribute.

    #     Args:
    #         btn (str): the button whose slot/connection/callback is to be defined.
    #         callback (function): callback function.

    #     Returns:
    #         bool: returns True if callback is successfully connected, otherwise it prints the exception and returns a False message.
    #     """
    #     try:
    #         btn = eval(f"self.{btn}")
    #         print(btn)
    #         btn.show()
    #         btn.clicked.connect(callback)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return False
    # gray = """qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #3f3f3f, stop : 0.091 #494949, stop : 0.182 #545454, stop : 0.273 #5f5f5f, stop : 0.364 #6a6a6a, stop : 0.455 #757575, stop : 0.545 #808080, stop : 0.636 #8c8c8c, stop : 0.727 #989898, stop : 0.818 #a4a4a4, stop : 0.909 #b0b0b0, stop : 1.0 #bcbcbc)"""