#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from turtle import bgcolor
from fig_dash import FigDLoad
FigDLoad("fig_dash::ui::__init__")

import os
import jinja2
from typing import *
from pathlib import Path
from functools import partial
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.titlebar import WindowTitleBar
# PyQt5 imports
from PyQt5.QtGui import QFontDatabase, QColor, QPalette, QIcon, QKeySequence, QRegion
from PyQt5.QtCore import Qt, QUrl, QSize, QEvent, pyqtSignal, QStringListModel, QRect, QPoint, QVariant, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QApplication, QMenu, QFrame, QAction, QWidget, QWidgetAction, QMainWindow, QTabBar, QTabWidget, QLabel, QToolButton, QVBoxLayout, QHBoxLayout, QGridLayout, QSystemTrayIcon, QScrollArea, QShortcut, QSlider, QLineEdit, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QSizePolicy, QCompleter, QStyle, QProxyStyle

# blank function.
def blank(*args, **kwargs): print("fig_dash::ui::__init__::blank :", args, kwargs)
class FigDShortcut(QShortcut):
    def __init__(self, keyseq: QKeySequence, 
                 parent: Union[None, QWidget]=None,
                 description: str="description"):
        super(FigDShortcut, self).__init__(keyseq, parent)
        self.description = description
        self.func = None

    def connect(self, func):
        self.activated.connect(func)
        self.func = func

    def activate(self):
        print(self.description + " activated")
        if self.func is not None: self.func()

# property animation based show/hide.
def smooth_transition(target: QWidget):
    def animated_show(self):
        import copy
        geometry = self.geometry()
        target_geometry = copy.deepcopy(geometry)
        target_geometry.setHeight(self.prehide_height)
        print(f"show: {geometry} -> {target_geometry}")
        # showing property animation.
        self.show_animation = QPropertyAnimation(self, b"geometry")
        # set duration, easing curve, start and end value.
        self.show_animation.setStartValue(geometry)
        self.show_animation.setEndValue(target_geometry)
        self.show_animation.setEasingCurve(QEasingCurve.OutExpo)
        # start animation.
        self.show_animation.start()
        self.setVisible(True)

    def animated_hide(self):
        import copy
        geometry = self.geometry()
        target_geometry = copy.deepcopy(geometry)
        target_geometry.setHeight(0)
        print(f"hide: {geometry} -> {target_geometry}")
        # hiding property animation.
        self.hide_animation = QPropertyAnimation(self, b"geometry")
        # set duration, start and end value.
        self.hide_animation.setStartValue(geometry)
        self.hide_animation.setEndValue(target_geometry)
        self.hide_animation.setEasingCurve(QEasingCurve.OutExpo)
        # start animation.
        self.hide_animation.start()
        self.setVisible(False)

    def unanimated_hide(self):
        self.prehide_height = self.height()
        self.hide()
    # set function.  
    setattr(target, "animated_show", animated_show)
    setattr(target, "animated_hide", animated_hide)
    setattr(target, "unanimated_hide", unanimated_hide)
    # print(f"target class: {target}")
    return target

FIGD_TABBAR_BACKGROUND = "#141414"
DASH_WIDGET_SCROLL_AREA = jinja2.Template("""
QWidget {
    color: #fff;
    border: 0px;
    background: transparent;
    font-family: 'Be Vietnam Pro';
    font-size: 16px;
}
QScrollArea {
    border: 0px;
    background-position: center;
}
QScrollBar:vertical {
    border: 0px solid #999999;
    width: 12px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0.1);
}
QScrollBar::handle:vertical {
    min-height: 0px;
    border: 0px solid red;
    border-radius: 0px;
    background-color: rgba(255, 255, 255, 0.25);
}
QScrollBar::handle:vertical:hover {
    background-color: rgba(255, 255, 255, 0.6);
}
QScrollBar::handle:horizontal {
    min-height: 0px;
    border: 0px solid red;
    border-radius: 0px;
    background-color: transparent;
}
QScrollBar::handle:horizontal:hover {
    background-color: rgba(255, 255, 255, 0.5);
}
QScrollBar::add-line:vertical {
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}""")
DASH_WIDGET_GROUP_BTN_STYLESHEET = jinja2.Template("""
QToolButton {
    color: #fff;
    border: 0px;
    font-size: 14px;
    background: transparent;
}
QToolButton:hover {
    color: #292929;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #eb5f34, stop: 0.9 #338fc0);
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}""")
DASH_WIDGET_GROUP = jinja2.Template("""
""")
TEXT_EDIT_CONTEXT_MENU_MAP = {
    "Forward": (
        FigD.icon("textedit/forward.svg"), 
        FigD.icon("textedit/forward_disabled.svg")        
    ),
    "Back": (
        FigD.icon("textedit/back.svg"), 
        FigD.icon("textedit/back_disabled.svg")        
    ),
    "Reload": (
        FigD.icon("textedit/reload.svg"), 
        FigD.icon("textedit/reload_disabled.png")        
    ),
    "Select All	Ctrl+A": (
        FigD.icon("textedit/select_all.png"), 
        FigD.icon("textedit/select_all_disabled.png")
    ),
    "Cu&t	Ctrl+X": (
        FigD.icon("textedit/cut.svg"),
        FigD.icon("textedit/cut_disabled.svg")
    ),
    "Cut	Ctrl+X": (
        FigD.icon("textedit/cut.svg"),
        FigD.icon("textedit/cut_disabled.svg")
    ),
    "Copy": (
        FigD.icon("textedit/copy.svg"),
        FigD.icon("textedit/copy_disabled.svg")
    ),
    "&Copy": (
        FigD.icon("textedit/copy.svg"),
        FigD.icon("textedit/copy_disabled.svg")
    ),
    "&Copy	Ctrl+C": (
        FigD.icon("textedit/copy.svg"),
        FigD.icon("textedit/copy_disabled.svg")
    ),
    "Undo	Ctrl+Z": (
        FigD.icon("textedit/undo.svg"),
        FigD.icon("textedit/undo_disabled.svg")
    ),
    "Redo	Ctrl+Shift+Z": (
        FigD.icon("textedit/redo.svg"),
        FigD.icon("textedit/redo_disabled.svg")
    ),
    "&Undo	Ctrl+Z": (
        FigD.icon("textedit/undo.svg"),
        FigD.icon("textedit/undo_disabled.svg")
    ),
    "&Redo	Ctrl+Shift+Z": (
        FigD.icon("textedit/redo.svg"),
        FigD.icon("textedit/redo_disabled.svg")
    ),
    "Paste	Ctrl+V": (
        FigD.icon("textedit/paste.svg"),
        FigD.icon("textedit/paste_disabled.svg")
    ),
    "&Paste	Ctrl+V": (
        FigD.icon("textedit/paste.svg"),
        FigD.icon("textedit/paste_disabled.svg")
    ),
    "Delete": (
        FigD.icon("textedit/delete.svg"),
        FigD.icon("textedit/delete_disabled.svg")
    ),
}
# blur effect class.
class BlurEffect(QGraphicsBlurEffect):
    shouldEnable = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watched = []

    def watchWidget(self, widget):
        widget.installEventFilter(self)
        self.watched.append(widget)

    def unwatchWidget(self, widget):
        if widget in self.watched:
            self.watched.remove(widget)
            self.update()

    def setEnabled(self, enabled):
        # in case you want to manually disable the effect, keep track of
        # the selected behavior
        self.shouldEnable = enabled
        super().setEnabled(enabled)

    def draw(self, qp):
        print(f"drawing blur for {qp} with radius: {self.blurRadius()}")
        rects = []
        for widget in self.watched:
            if widget.isVisible():
                rect = widget.rect()
                if rect.isNull():
                    continue
                # map the widget geometry to the window
                rect.translate(
                    widget.mapTo(widget.window(), QPoint()))
                rects.append(rect)
            if not self.isEnabled() and self.shouldEnable:
                super().setEnabled(True)
        if not rects:
            # no valid rect to be used, disable the effect if we should
            if not self.shouldEnable:
                super().setEnabled(False)
            # otherwise, keep drawing the source with the effect applied
            # to the whole area of the widget
            else:
                self.drawSource(qp)
        else:
            qp.save()
            # create a region that includes all rects
            rectRegion = QRegion()
            for rect in rects:
               rectRegion |= QRegion(rect) 
            # clip the effect painting to the region
            qp.setClipRegion(rectRegion)
            # call the default implementation, which will draw the effect
            super().draw(qp)
            # get the full region that should be painted
            fullRegion = QRegion(qp.viewport())
            # and subtract the effect rectangle used before
            fullRegion -= rectRegion
            qp.setClipRegion(fullRegion)
            # draw the *source*, which has no effect applied
            self.drawSource(qp)
            qp.restore()

    def eventFilter(self, source, event):
        # update the effect whenever a widget changes its geometry or
        # becomes visible
        if event.type() in (QEvent.Resize, QEvent.Move, 
            QEvent.Show) and source.isVisible():
                super().setEnabled(True)
                self.update()
        # if a widget is going to be deleted, remove it from the list
        # of watched list; this is **VERY** important
        elif event.type() == QEvent.DeferredDelete:
            self.unwatchWidget(source)
        return super().eventFilter(source, event)

def setAccentColorAlpha(bg, alpha: int=150):
    if bg == "transparent": return bg
    qt_grad_elem = bg.split("stop")[0].strip()
    hex_color_list = ["#"+i.split("#")[-1].split()[0].replace(")","").replace(",","").replace(";","") for i in bg.split("stop")[1:]]
    stop = 0
    for hex_str in hex_color_list:
        qc = QColor(hex_str)
        qt_grad_elem += f" stop : {stop:.3f} rgba({qc.red()}, {qc.green()}, {qc.blue()}, {alpha}),"
        stop += 1/len(hex_color_list)
    qt_grad_elem = qt_grad_elem[:-1]
    qt_grad_elem += ")"
    # FigD.debug(qt_grad_elem)
    return qt_grad_elem

def extractFromAccentColor(bg, where="back"):
    if ("qlineargradient" in bg or "qconicalgradient" in bg) and (where=="back"):
        extractedColor = bg.split(":")[-1].strip()
        extractedColor = extractedColor.split()[-1]
        extractedColor = extractedColor.split(")")[0]
        extractedColor = extractedColor.strip()
    elif ("qlineargradient" in bg or "qconicalgradient" in bg) and (where=="front"):
        extractedColor = bg.split("stop")[1]
        extractedColor = extractedColor.split("#")[-1]
        extractedColor = extractedColor.split(",")[0]
        extractedColor = "#"+extractedColor.strip()
    else: 
        extractedColor = "white" 

    return extractedColor

def accentColorFromBackground(bgImagePath: str):
    import extcolors
    colors, pixel_count = extcolors.extract_from_path(bgImagePath)
    accentColor: str = "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1,"
    sortedColors = sorted(colors, key=lambda x: x[1], reverse=True)
    cum_count, normColors = 0, []
    for rgb, count in sortedColors:
        cum_count += count
        normColors.append((rgb, cum_count/pixel_count))
    colorList: list = [c[0] for c in normColors]
    stopsList: list = [c[1] for c in normColors]
    for color, stop in zip(colorList, stopsList):
        accentColor += f" stop : {stop:.3f} rgb{color},"
    accentColor = accentColor[:-1]
    accentColor += ")" # print(accentColor)
    
    return accentColor

def styleTextEditMenuIcons(menu):
    """substitute TextEdit/LineEdit icons for consistent styling."""
    for action in menu.actions():
        # print(action.text(), action.text() in TEXT_EDIT_CONTEXT_MENU_MAP)
        icon, icon_disabled = TEXT_EDIT_CONTEXT_MENU_MAP.get(
            action.text(), 
            ("NOT_FOUND","NOT_FOUND")
        )
        if icon == "NOT_FOUND" and icon_disabled == "NOT_FOUND":
            for key in TEXT_EDIT_CONTEXT_MENU_MAP:
                if key.startswith(action.text()):
                    icon, icon_disabled = TEXT_EDIT_CONTEXT_MENU_MAP[key]
        if action.isEnabled(): 
            action.setIcon(QIcon(icon))
        else: 
            action.setIcon(QIcon(icon_disabled))

    return menu

# proxy style for context menu.
class FigDMenuProxyStyle(QProxyStyle):
    def drawControl(self, element, option, painter, widget=None):
        shortcut = ""
        if element == QStyle.CE_MenuItem:
            vals = option.text.split("\t")
            if len(vals) == 2:
                text, shortcut = vals
                option.text = text
        super(FigDMenuProxyStyle, self).drawControl(element, option, painter, widget)
        if shortcut:
            margin = 10 # QStyleHelper::dpiScaled(5)
            self.proxy().drawItemText(painter, option.rect.adjusted(margin, 0, -margin, 0), 
                Qt.AlignRight | Qt.AlignVCenter,
                option.palette, option.state & QStyle.State_Enabled, 
                shortcut, QPalette.Text)

def styleContextMenu(menu, accent_color: str="rgb(255,255,255)", 
                     icon_size: int=24, margin: int=10, padding: int=5,
                     opacity: float=0.7, font_size: int=18):
    menu.setAttribute(Qt.WA_TranslucentBackground)
    menu.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
    menu.setObjectName("FigDMenu")
    border_color = extractFromAccentColor(accent_color)
    styleSheet = jinja2.Template("""
    QMenu#FigDMenu {
        /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, {{ OPACITY }}), stop : 0.143 rgba(22, 22, 22, {{ OPACITY }}), stop : 0.286 rgba(27, 27, 27, {{ OPACITY }}), stop : 0.429 rgba(32, 32, 32, {{ OPACITY }}), stop : 0.571 rgba(37, 37, 37, {{ OPACITY }}), stop : 0.714 rgba(41, 41, 41, {{ OPACITY }}), stop : 0.857 rgba(46, 46, 46, {{ OPACITY }}), stop : 1.0 rgba(51, 51, 51, {{ OPACITY }})); */
        background: rgba(0, 0, 0, {{ OPACITY }});
        background-image: url(/home/atharva/GUI/fig-dash/resources/icons/textedit/NoiseGaussBlur(5).png);
        color: #fff;
    	padding: {{ MARGIN }}px;
        font-size: {{ FONT_SIZE }}px;
        font-family: "Be Vietnam Pro";
        border: none;
        border-radius: 15px;
    }
    QMenu#FigDMenu:right-arrow {
        image: url(/home/atharva/GUI/fig-dash/resources/icons/textedit/chevron.svg);
    }
    QMenu#FigDMenu::right-arrow:selected {
        image: url(/home/atharva/GUI/fig-dash/resources/icons/textedit/chevron_hover.svg);
    }
    QMenu#FigDMenu::item {
        background: transparent;
        padding: {{ PADDING }}px;
        /* border: 1px solid transparent; */
    }
    QMenu#FigDMenu::item:selected {
    	color: #292929; 
        border-radius: 5px;
        /* border: 1px solid {{ BORDER_COLOR }}; */
    	background-color: {{ ACCENT_COLOR_WITH_ALPHA }}; 
    }
    QMenu#FigDMenu:separator {
    	background: #484848;
    }""").render(
        FONT_SIZE=font_size, PADDING=padding, 
        ICON_SIZE=icon_size, OPACITY=opacity,
        ACCENT_COLOR_WITH_ALPHA=accent_color,
        BORDER_COLOR=border_color, MARGIN=margin,
    )
    menu.setStyleSheet(styleSheet)
    # create shadow with color derived from accent color.
    # shadowColor = QColor(extractFromAccentColor(accent_color))
    shadow = QGraphicsDropShadowEffect()
    # shadow.setColor(Qt.white)
    shadow.setColor(QColor("#fff"))
    shadow.setBlurRadius(5)
    shadow.setOffset(0, 0)
    # set shadow graphics effect.
    menu.setGraphicsEffect(shadow)

    palette = menu.palette()
    palette.setColor(QPalette.Base, QColor(48,48,48))
    palette.setColor(QPalette.Text, QColor(125,125,125))
    palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    palette.setColor(QPalette.Window, QColor(255,255,255))
    palette.setColor(QPalette.Highlight, QColor(235,95,52))
    menu.setPalette(palette)

    return menu

# fig style menu with right side text alignment.
class FigDMenu(QMenu):
    def __init__(self, *args, **kwargs):
        super(FigDMenu, self).__init__(*args, **kwargs)
        # style context menu using proxy style. 
        self._proxy = FigDMenuProxyStyle(self.style())
        self.setStyle(self._proxy)

# dash slider (has a label to directly enter values).
class DashSlider(QWidget):
		def __init__(self, text: str, icon: str="", icon_size: Tuple[int,int]=(25,25), minm: int=0, maxm: int=50, value: int=100, accent_color: str="yellow", parent: Union[QWidget, None]=None):
				super(DashSlider, self).__init__(parent)
				# main layout.
				self.vboxlayout = QVBoxLayout()
				self.vboxlayout.setContentsMargins(0, 0, 0, 0)
				self.vboxlayout.setSpacing(0)
				# upper widget with hboxlayout.
				self.hboxlayout = QHBoxLayout()
				self.hboxlayout.setContentsMargins(0, 0, 0, 0)
				self.hboxlayout.setSpacing(0)
				# slider widget.
				self.slider = QSlider(Qt.Horizontal)
				self.slider.setMinimum(minm)
				self.slider.setMaximum(maxm)
				self.slider.setValue(value)
				self.slider.setMinimumWidth(200)
				self.slider.valueChanged.connect(self.updateEffect)
		
				self.label = QLabel(text)
				self.label.setStyleSheet("""
				QLabel {
						color: #fff;
						font-size: 17px;
				}""")
				# slider readout.
				self.readout = QLineEdit()
				self.readout.setText(str(value))
				self.readout.setStyleSheet("""
				QLineEdit {
                        color: #fff;
						font-size: 16px;
				}""")
				self.readout.returnPressed.connect(self.setEffect)
				self.readout.setMaximumWidth(40)
				# display icon.
				self.icon = QLabel()
				self.icon.setPixmap(
                    FigD.Icon(icon).pixmap(
                        QSize(*icon_size)
				))
				# hboxwidget.
				self.hboxwidget = QWidget()
				self.hboxwidget.setLayout(self.hboxlayout)
				# build hboxlayout.
				self.hboxlayout.addWidget(self.icon)
				self.hboxlayout.addWidget(self.readout)
				self.hboxlayout.addWidget(self.slider)
				self.hboxlayout.addStretch(1)
				self.vboxlayout.addWidget(self.hboxwidget, 0, Qt.AlignCenter)
				self.vboxlayout.addWidget(self.label, 0, Qt.AlignCenter)
				self.vboxlayout.addStretch(1)
				self.setObjectName("DashSlider")
				self.setStyleSheet("""
				QWidget#DashSlider {
						color: #fff;
						font-family: 'Be Vietnam Pro';
						background: transparent;
				}""")
				self.setLayout(self.vboxlayout)
				# set slider palette color.
				background = accent_color
				if "qlineargradient" in background:
						sliderHandleColor = background.split(":")[-1].strip()
						sliderHandleColor = sliderHandleColor.split()[-1].split(")")[0]
						sliderHandleColor = sliderHandleColor.strip()
				else: 
						sliderHandleColor = background
				palette = QPalette()
				palette.setColor(QPalette.Window, QColor(0,255,255))
				palette.setColor(QPalette.Button, QColor(sliderHandleColor))
				palette.setColor(QPalette.Highlight, QColor(sliderHandleColor))
				self.slider.setPalette(palette)

		def setEffect(self):
				try: 
						value = float(self.readout.text())
						self.slider.setValue(value)
				except Exception as e:
						scopeStr = "\x1b[31;1mui::__init__::DashSlider.setEffect:\x1b[0m"
						print(scopeStr, e)

		def updateEffect(self, value):
				self.readout.setText(str(value))
				pass

# dash widget group button.
class DashWidgetGroupBtn(QToolButton):
    '''Dash Widget button'''
    mouseExited = pyqtSignal()
    mouseEntered = pyqtSignal() 
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashWidgetGroupBtn, self).__init__(parent)
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        icon = args.get("icon")
        text = args.get("text")
        style = args.get("style")
        fg_color = args.get("fg_color", "#eb5f34")
        background = args.get("background", "transparent")
        border_color = extractFromAccentColor(background)
        stylesheet = args.get("stylesheet")
        self.is_text_button = True
        self.hover_response = "background"
        if icon:
            self.is_text_button = False
            self.inactive_icon = args["icon"]
            stem, ext = os.path.splitext(Path(args["icon"]))
            self.active_icon = f"{stem}_active{ext}"
            if os.path.exists(FigD.icon(self.active_icon)):
                self.hover_response = "foreground"
            else:
                self.active_icon = FigD.icon(f"{stem}_hover{ext}")
            self.setIcon(FigD.Icon(self.inactive_icon))
            # print(f"found {self.active_icon} {self.hover_response}")
        if text: self.setText(args["text"])
        if style: self.setToolButtonStyle(style)
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStatusTip(tip)
        bg_with_alpha = setAccentColorAlpha(background, alpha=150)
        # stylesheet attributes.
        if stylesheet:
            self.setStyleSheet(stylesheet)
        elif self.hover_response == "background":
            stylesheet = jinja2.Template('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                border-radius: 2px;
                background: transparent;
                border: 1px solid transparent;
            }
            QToolButton:hover {
                color: #292929;
                border: 1px solid {{ border_color }};
                background: {{ background }};
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''').render(
                background=bg_with_alpha,
                border_color=border_color,
            )
            self.setStyleSheet(stylesheet)
            # /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
        else:
            self.fg_color = fg_color
            self.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                background: transparent;
            }
            QToolButton:hover {
                color: '''+self.fg_color+''';
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''')

    def leaveEvent(self, event):
        if not self.is_text_button:
            self.setIcon(FigD.Icon(self.inactive_icon))
        self.mouseExited.emit()
        super(DashWidgetGroupBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        if not self.is_text_button and os.path.exists(self.active_icon):
            self.setIcon(FigD.Icon(self.active_icon))
        self.mouseEntered.emit()
        super(DashWidgetGroupBtn, self).enterEvent(event)

# dash widget group.
class DashWidgetGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: str="Widget Group", 
                 accent_color: str="gray"):
        super(DashWidgetGroup, self).__init__(parent)
        self.accent_color = accent_color
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.__widget_list = []
        self.group = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(2)
        self.group.setLayout(self.layout)
        self.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
            margin-left: 5px;
            margin-right: 5px;
        }""")
        layout.addStretch(1)
        layout.addWidget(self.group)
        layout.addWidget(self.Label(name))
        self.setLayout(layout)

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def addWidget(self, *args, **kwargs):
        self.layout.addWidget(*args, **kwargs)
        self.__widget_list.append(args[0])

    def memberAt(self, index: int) -> Union[QWidget, None]:
        try:
            return self.__widget_list[index]
        except IndexError as e:
            print("ui::__init__::DashWidgetGroup.widgetAt", e)
            return None

    def Label(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #6e6e6e; /* #eb5f34; */
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }''')
        self.groupLabelName = name

        return name

    def initBtnGroup(self, btn_args, orient="horizontal", 
                     alignment_flag=None, spacing=None):
        btnGroup = QWidget()
        btnGroup.btns = []
        if orient == "horizontal":
            layout = QHBoxLayout()
        elif orient == "vertical":
            layout = QVBoxLayout()
        if spacing is not None:
            layout.setSpacing(spacing)
            # print(f"{self.groupLabelName.text()}: layout.setSpacing({spacing})")
        layout.setContentsMargins(0, 0, 0, 0)
        btnGroup.layout = layout
        btnGroup.setLayout(layout)
        btnGroup.setStyleSheet('''
        QWidget {
            color: #fff;
            border: 0px;
            font-size: 10px;
            background: transparent;
        }''')
        layout.addStretch(1)
        for args in btn_args:
            btn = self.initBtn(**args)
            btnGroup.btns.append(btn)
            if alignment_flag is None:
                layout.addWidget(btn, 0, Qt.AlignCenter)
            else:
                layout.addWidget(btn, 0, alignment_flag)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def wrapInScrollArea(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("border: 2px solid gray;")

        return scrollArea

    def initBtnGrid(self, btn_args, spacing=None, 
                    alignment_flag=None):
        btnGrid = QWidget()
        btnGrid.btns = []
        layout = QGridLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        if spacing:
            layout.setSpacing(spacing)
        else: layout.setSpacing(0)
        btnGrid.setLayout(layout)
        btnGrid.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            font-size: 10px;
            background: transparent;
        }""")
        # print(f"btn_args: {btn_args}")
        for i, btn_row_args in enumerate(btn_args):
            for j, args in enumerate(btn_row_args):
                islabel = args.get("label", False)
                stretch = args.get("stretch", False)
                if stretch: layout.addStretch(1)
                elif islabel:
                    text = args.get("text", "text not set")
                    label = QLabel(text)
                    label.setStyleSheet("""
                    QLabel {
                        color: #fff;
                        border: 0px;
                        font-size: 14px;
                        background: transparent;
                    }""")
                    layout.addWidget(label)
                else:
                    btn = self.initBtn(**args)
                    btnGrid.btns.append(btn)
                    if alignment_flag is None:
                        layout.addWidget(btn, i, j, alignment=Qt.AlignCenter)
                    else:
                        layout.addWidget(btn, i, j, alignment=alignment_flag)
        scrollArea = self.wrapInScrollArea(btnGrid)
        scrollArea.grid = btnGrid

        return scrollArea

    def setBackgroundColor(self, color):
        palette = self.palette()
        if isinstance(color, str): 
            color = QColor(color)
        elif isinstance(color, tuple): 
            color = QColor(*color)
        palette.setColor(QPalette.Window, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def enterEvent(self, event):
        """on entering highlight the group's background and it's name"""
        self.setBackgroundColor((255,255,255,20))
        self.groupLabelName.setStyleSheet("""
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: """+self.accent_color+""";
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }""")
        super(DashWidgetGroup, self).enterEvent(event)

    def leaveEvent(self, event):
        """on exiting restore the group's default styling"""
        # print("\x1b[34;1mleaveEvent\x1b[0m")
        self.setBackgroundColor((255,255,255,0))
        self.groupLabelName.setStyleSheet("""
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #6e6e6e;
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }""")
        super(DashWidgetGroup, self).leaveEvent(event)

    def initBtn(self, **args):
        return DashWidgetGroupBtn(self, **args)

# simple group button for DashSimpleGroup.
# dash widget group button.
class DashSimpleGroupBtn(QToolButton):
    '''Dash simple group button'''
    mouseExited = pyqtSignal()
    mouseEntered = pyqtSignal() 
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(DashSimpleGroupBtn, self).__init__(parent)
        # main arguments.
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        icon = args.get("icon")
        accent_color = args.get("accent_color", "transparent")
        # whether button/function is enabled or disabled.
        self._is_enabled = True
        self.accent_color = accent_color
        # all icon paths.
        fname_wout_ext, ext = os.path.splitext(icon)
        self.icon_path = FigD.icon(icon)
        self.hover_icon_path = f"{fname_wout_ext}_active{ext}"
        self.disabled_icon_path = f"{fname_wout_ext}_disabled{ext}"
        # reset if hover/disabled icon paths don't exist.
        if not os.path.exists(self.hover_icon_path):
            self.hover_icon_path = self.icon_path
        if not os.path.exists(self.disabled_icon_path):
            self.disabled_icon_path = self.icon_path
        # set main icon.
        self.setIcon(FigD.Icon(self.inactive_icon))
        # border color and background color.
        border_color = extractFromAccentColor(accent_color)
        bg_alpha = setAccentColorAlpha(accent_color, alpha=150)
        self.border_color = border_color
        self.bg_alpha = bg_alpha
        # set stuff.
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.setIconSize(QSize(*size))
        self.setStyleSheet(jinja2.Template("""
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
        }
        QToolButton:hover {
            color: #292929;
            border: 1px solid {{ border_color }};
            background: {{ background }};
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }""").render(
                background=bg_alpha,
                border_color=border_color,
            )
        )
        # /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
    def isEnabled(self):
        return self._is_enabled

    def setEnabled(self, value: bool):
        self._is_enabled = value
        if value:
            self.setIcon(FigD.Icon(self.icon_path))
            self.setStyleSheet(jinja2.Template("""
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                border-radius: 2px;
                background: transparent;
            }
            QToolButton:hover {
                color: #292929;
                border: 1px solid {{ border_color }};
                background: {{ background }};
                /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }""").render(
                    background=self.bg_alpha,
                    border_color=self.border_color,
                )
            )
        else:
            self.setIcon(FigD.Icon(self.disabled_icon_path))
            self.setStyleSheet(jinja2.Template("""
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                border-radius: 2px;
                background: transparent;
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }""").render(
                    background=self.bg_alpha,
                    border_color=self.border_color,
                )
            )

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.icon_path))
        self.mouseExited.emit()
        super(DashWidgetGroupBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.hover_icon_path))
        self.mouseEntered.emit()
        super(DashWidgetGroupBtn, self).enterEvent(event)

# dash widget ribbon menu.
class DashRibbonMenu(QWidget):
    def __init__(self, group_names: List[str]=[], 
                 parent: Union[None, QWidget]=None,
                 accent_color: str="gray", where: str="back",
                 contents_margins=(5, 0, 5, 0)):
        super(DashRibbonMenu, self).__init__(parent)
        self.accent_color = accent_color
        # drop shadow.
        drop_shadow = self.createDropShadow(accent_color, where)
        self.setGraphicsEffect(drop_shadow)
        self.separators = []
        # create the scoll area.
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area.setStyleSheet(DASH_WIDGET_SCROLL_AREA.render())
        self.setAttribute(Qt.WA_TranslucentBackground)
        # create Ribbon Menu main layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(1)
        # group names and group widget map/
        self.__group_names = group_names
        self.__group_widget_map = {}
        for name in self.__group_names[:-1]:
            self.__group_widget_map[name] = DashWidgetGroup(
                parent=self, name=name, 
                accent_color=accent_color
            )
            self.hboxlayout.addWidget(self.__group_widget_map[name])
            self.hboxlayout.addWidget(self.addSeparator())
        name = self.__group_names[-1]
        self.__group_widget_map[name] = DashWidgetGroup(
            parent=self, name=name,
            accent_color=accent_color,
        )
        self.hboxlayout.addWidget(self.__group_widget_map[name])
        self.hboxlayout.addStretch(1)
        # create main widget and set it's layout.
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.hboxlayout)
        self.__scroll_area.setWidget(self.main_widget)
        # init and build vboxlayout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(*contents_margins)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.addWidget(self.__scroll_area)
        # set layout.
        self.setLayout(self.vboxlayout)

    def createDropShadow(self, accent_color: str, where: str="back"):
        drop_shadow_color = extractFromAccentColor(accent_color, where=where)
        drop_shadow = QGraphicsDropShadowEffect()
        drop_shadow.setColor(QColor(drop_shadow_color))
        drop_shadow.setBlurRadius(10)
        drop_shadow.setOffset(0, 0)

        return drop_shadow

    def __iter__(self):
        for group_name in self.__group_widget_map:
            yield group_name

    def addSeparator(self, height: int=110):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #292929;''')
        sep.setLineWidth(1)
        sep.setMaximumHeight(110)
        self.separators.append(sep)

        return sep

    def contextMenuEvent(self, event):
        self.contextMenu = QMenu()
        self.contextMenu = styleContextMenu(
            self.contextMenu, self.accent_color, 
            padding=2, font_size=17,
        )
        self.contextMenu.addAction(
            f"Minimize ribbon",
            self.hide,
        )
        self.contextMenu.addAction(
            f"Show all groups     ",
            self.showAllGroups,
        )
        self.contextMenu.addAction(
            "Hide all groups   ",
            self.hideAllGroups,
        )
        def chain(*funcs):
            for func in funcs: func()
        i = 0
        group_widget_items = [(k,v) for k,v in self.__group_widget_map.items()]
        for group_name, widget_group in group_widget_items[:-1]:
            sep = self.separators[i]
            if widget_group.isVisible():
                self.contextMenu.addAction(
                    FigD.Icon("widget/checkmark.svg"), 
                    f"{group_name}", partial(chain, widget_group.hide, sep.hide)
                )
            else:
                self.contextMenu.addAction(f"{group_name}", partial(chain, widget_group.show, sep.show))
            i += 1
        group_name, widget_group = group_widget_items[-1]
        if widget_group.isVisible():
            self.contextMenu.addAction(
                FigD.Icon("widget/checkmark.svg"), 
                f"{group_name}", widget_group.hide
            )
        else:
            self.contextMenu.addAction(f"{group_name}", widget_group.show)
        self.contextMenu.popup(event.globalPos())

    def hideAllGroups(self):
        for widget_group in self.__group_widget_map.values():
            widget_group.hide()

    def showAllGroups(self):
        for widget_group in self.__group_widget_map.values():
            widget_group.show()

    def hideGroup(self, groupName):
        self.widgetGroupAt(groupName).hide()

    def showGroup(self, groupName):
        self.widgetGroupAt(groupName).show()

    def setFixedHeight(self, height: int):
        for sep in self.separators:
            sep.setMaximumHeight(height-2*10)
        super(DashRibbonMenu, self).setFixedHeight(height)

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def widgetGroupAt(self, group_name: str=""):
        return self.__group_widget_map[group_name]

    def addWidgetGroup(self, group_name: str="View", 
                       widgets: List[Tuple[QWidget, dict]]=[]):
        widget_group = self.__group_widget_map[group_name]
        for widget, args in widgets:
            if isinstance(widget, QWidget):
                widget_group.addWidget(widget, **args)
            elif isinstance(widget, dict):
                btn = widget_group.initBtn(**widget)
                widget_group.addWidget(btn, **args)                
            elif isinstance(widget, list):
                if isinstance(widget[0], list):
                    btnGrid = widget_group.initBtnGrid(btn_args=widget, **args)
                    widget_group.addWidget(btnGrid, 0, Qt.AlignVCenter)
                else:
                    btnGroup = widget_group.initBtnGroup(btn_args=widget, **args)
                    widget_group.addWidget(btnGroup, 0, Qt.AlignVCenter)

        return widget_group

# widget group for simplified dash menu.
class DashSimpleGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: str="Group", accent_color: str="gray"):
        super(DashSimpleGroup, self).__init__(parent=parent)
        self.accent_color = accent_color
        # layout of simple group.
        self.__name = name
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(5)
        # name of the simple group.
        self.groupNameBtn = self.initGroupName(name)
        # build layout.
        self.hboxlayout.addWidget(self.groupNameBtn)
        # set layout.
        self.setLayout(self.hboxlayout)

    def addWidget(self, widget):
        i = self.hboxlayout.count()
        self.hboxlayout.insertWidget(i-1, widget)

    def addBtn(self, **args):
        btn = DashSimpleGroupBtn(**args)
        self.addWidget(btn)

        return btn

    def groupName(self) -> str:
        return self.__name

    def setGroupName(self, name: str):
        self.__name = name
        self.groupNameBtn.setText(name)

    def initGroupName(self, name) -> QLabel:
        groupNameBtn = QToolButton(name)
        groupNameBtn.setText(name)
        groupNameBtn.setAlignment(Qt.AlignCenter)
        groupNameBtn.setStyleSheet("""
        QToolButton {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #6e6e6e; /* #eb5f34; */
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
        }""")

        return groupNameBtn
         
    def enterEvent(self, event):
        self.groupNameLabel.show()
        super(DashSimpleGroup, self).enterEvent(event)

    def leaveEvent(self, event):
        self.groupNameLabel.hide()
        super(DashSimpleGroup, self).leaveEvent(event)

    def widgetGroupAt(self, group_name: str=""):
        return self.__group_widget_map[group_name]

    def addWidgetGroup(self, group_name: str="View", 
                       widgets: List[Tuple[QWidget, dict]]=[]):
        widget_group = self.__simple_group_map[group_name]
        for widget, args in widgets:
            if isinstance(widget, QWidget):
                widget_group.addWidget(widget, **args)
            elif isinstance(widget, dict):
                btn = widget_group.initBtn(**widget)
                widget_group.addWidget(btn, **args)

        return widget_group

# simplified ribbon menu.
class DashSimplifiedMenu(QWidget):
    def __init__(self, group_names: List[str]=[], 
                 parent: Union[None, QWidget]=None,
                 accent_color: str="gray", where: str="back",
                 contents_margins=(5, 0, 5, 0)):
        super(DashRibbonMenu, self).__init__(parent)
        self.accent_color = accent_color
        # drop shadow.
        drop_shadow = self.createDropShadow(accent_color, where)
        self.separators = []
        # create the scoll area.
        self.initScrollArea()
        # create Ribbon Menu main layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(1)
        # group names and group widget map/
        self.__group_names = group_names
        self.__simple_group_map = {}
        for name in self.__group_names[:-1]:
            self.__simple_group_map[name] = DashSimpleGroup(
                parent=self, name=name, 
                accent_color=accent_color
            )
            self.hboxlayout.addWidget(self.__sample_group_map[name])
            self.hboxlayout.addWidget(self.addSeparator())
        name = self.__group_names[-1]
        self.__simple_group_map[name] = DashSimpleGroup(
            parent=self, name=name,
            accent_color=accent_color,
        )
        self.hboxlayout.addWidget(self.__sample_group_map[name])
        self.hboxlayout.addStretch(1)
        # create main widget and set it's layout.
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.hboxlayout)
        self.__scroll_area.setWidget(self.main_widget)
        # init and build vboxlayout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(*contents_margins)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.addWidget(self.__scroll_area)
        # set stuff.
        self.setLayout(self.vboxlayout)
        self.setGraphicsEffect(drop_shadow)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def __iter__(self):
        for group_name in self.__simple_group_map:
            yield group_name

    def contextMenuEvent(self, event):
        self.contextMenu = QMenu()
        self.contextMenu = styleContextMenu(
            self.contextMenu, self.accent_color, 
            padding=2, font_size=17,
        )
        self.contextMenu.addAction(f"Minimize ribbon", self.hide)
        self.contextMenu.addAction(f"Show all groups     ", self.showAllGroups)
        self.contextMenu.addAction("Hide all groups   ", self.hideAllGroups)
        def chain(*funcs): 
            for func in funcs: func()
        i = 0
        group_items = [(k,v) for k,v in self.__simple_group_map.items()]
        for group_name, simple_group in group_items[:-1]:
            sep = self.separators[i]
            if simple_group.isVisible():
                self.contextMenu.addAction(
                    FigD.Icon("widget/checkmark.svg"), f"{group_name}", 
                    partial(chain, simple_group.hide, sep.hide)
                )
            else:
                self.contextMenu.addAction(
                    f"{group_name}", partial(chain, 
                    simple_group.show, sep.show)
                )
            i += 1
        group_name, simple_group = group_items[-1]
        if simple_group.isVisible():
            self.contextMenu.addAction(
                FigD.Icon("widget/checkmark.svg"), 
                f"{group_name}", simple_group.hide
            )
        else:
            self.contextMenu.addAction(
                f"{group_name}", 
                simple_group.show
            )
        self.contextMenu.popup(event.globalPos())

    def hideAllGroups(self):
        for simple_group in self.__simple_group_map.values():
            simple_group.hide()

    def showAllGroups(self):
        for simple_group in self.__simple_group_map.values():
            simple_group.show()

    def setFixedHeight(self, height: int):
        for sep in self.separators:
            sep.setMaximumHeight(height-2*10)
        super(DashRibbonMenu, self).setFixedHeight(height)

    def hideGroup(self, groupName):
        self.widgetGroupAt(groupName).hide()

    def showGroup(self, groupName):
        self.widgetGroupAt(groupName).show()

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def addSeparator(self, height: int=110):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #292929;''')
        sep.setLineWidth(0.5)
        sep.setMaximumHeight(110)
        self.separators.append(sep)

        return sep

    def initScrollArea(self):
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area.setStyleSheet(DASH_WIDGET_SCROLL_AREA.render())

    def createDropShadow(self, accent_color: str, where: str="back"):
        drop_shadow_color = extractFromAccentColor(accent_color, where=where)
        drop_shadow = QGraphicsDropShadowEffect()
        drop_shadow.setColor(QColor(drop_shadow_color))
        drop_shadow.setBlurRadius(10)
        drop_shadow.setOffset(0, 0)

        return drop_shadow

# FigD animated toggle.
class FigDToggle(QWidget):
    def __init__(self, text: str="", state1: str="on", 
                 state2: str="off", accent_color: str="gray", 
                 where="back", parent: Union[None, QWidget]=None):
        super(FigDToggle, self).__init__(parent)
        from fig_dash.ui.titlebar import extractSliderColor
        from fig_dash.ui.widget.boolean_toggle import AnimatedToggle
        
        self.accent_color = accent_color
        # horizontal layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(5)
        # toggle name.
        label_stylesheet = """
        QLabel {
            color: #fff;
            font-size: 18px;
            background: transparent;
            font-family: "Be Vietnam Pro";
        }"""
        self.label = QLabel()
        self.label.setStyleSheet(label_stylesheet)
        self.label.setText("       "+text)
        self.state1 = QLabel()
        self.state1.setStyleSheet(label_stylesheet)
        self.state1.setText(state1)
        self.state2 = QLabel()
        self.state2.setStyleSheet(label_stylesheet)
        self.state2.setText(state2)
        # actual animated toggle widget.
        self.toggle = AnimatedToggle()
        checked_color = extractSliderColor(
            accent_color, 
            where=where,
        )
        self.activated_color = checked_color
        # auto save toggle button.
        self.toggle = AnimatedToggle(
            checked_color=checked_color,
            pulse_checked_color=checked_color,
        )
        # build layout.
        self.hboxlayout.addWidget(self.label)
        self.addSeparator()
        self.hboxlayout.addStretch(1)
        self.hboxlayout.addWidget(self.state1)
        self.hboxlayout.addWidget(self.toggle, 1)
        self.hboxlayout.addWidget(self.state2)
        self.hboxlayout.addStretch(1)
        # set layout.
        self.setLayout(self.hboxlayout)

    def addSeparator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #484848;''')
        sep.setLineWidth(1)
        self.hboxlayout.addWidget(sep)

# slider style.
FIGD_SLIDER_STYLE = jinja2.Template(r"""
QSlider {
    margin: 5px 0px;
}
QSlider::groove:horizontal {
    height: 2px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
}
QSlider::sub-page:horizontal {
    background: {{ SLIDER_COLOR }};
}
QSlider::add-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
}
QSlider::handle:horizontal {
    border: 1px solid #929292;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #292929, stop:1 #484848);
    width: 14px;
    margin: -7px 1px; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 8px;
}""")
# margin = (2*border + width - grooveHeight)/2
# borderRadius = (width + 2*border)/2
# settings slider.  
class FigDSlider(QWidget):
    changed = pyqtSignal(float)
    updatedSlider = pyqtSignal()
    updatedReadout = pyqtSignal()
    displayChanged = pyqtSignal(int)
    def __init__(self, text: str="", value: int=0, minm: int=0, 
                 maxm: int=100, plus: bool=False, minus: bool=False,
                 accent_color: str="gray", orient: str="horizontal",
                 where: str="back", parent: Union[None, QWidget]=None,
                 set_status_tip: bool=True, btns_list: List[QToolButton]=[]):
        super(FigDSlider, self).__init__(parent)
        self.accent_color = accent_color
        self.vboxlayout = QVBoxLayout()
        self.hboxlayout = QHBoxLayout()
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        # slider name.
        if text != "":
            self.label = QLabel()
            self.label.setStyleSheet("""
            QLabel {
                color: #fff;
                font-size: 18px;
                background: transparent;
                font-family: "Be Vietnam Pro";
            }""")
            self.label.setText("      "+text)
            self.hboxlayout.addWidget(self.label)
        # horizontal slider area box.
        self.sliderbox = QWidget()
        self.sliderbox.setStyleSheet("""
        QWidget {
            color: #fff;
            padding: 5px;
            padding-left: 0px;
            font-size: 17px;
            background: transparent;
            font-family: "Be Vietnam Pro";
        }""")
        self.sliderbox.setLayout(self.hboxlayout)
        # create slider.
        if orient == "horizontal":
            self.slider = QSlider(Qt.Horizontal)
        elif orient == "vertical":
            self.slider = QSlider(Qt.Vertical)
        self.slider.setFixedWidth(90)
        self.slider.setValue(value)
        self.slider.setMinimum(minm)
        self.slider.setMaximum(maxm)
        # slider current value.
        self.readout = QLineEdit()
        self.readout.setFixedWidth(50)
        self.readout.setText(str(value))
        self.readout.setAlignment(Qt.AlignLeft)
        self.readout.setStyleSheet("""
        QLineEdit {
            padding: 0px;
            color: #929292;
            font-size: 16px;
            font-weight: bold;
            border-radius: 2px;
            selection-color: #292929;
            selection-background-color: """+self.accent_color+""";
        }""")
        # build horizontal layout (slider+readout)
        self.addSeparator()
        self.hboxlayout.addWidget(
            self.readout, 0, 
            Qt.AlignVCenter
        )
        if minus:
            self.minusBtn = self.initSliderBoxBtn(
                icon="widget/minus.svg", tip="decrease slider value",
                accent_color=accent_color, where=where,
                set_status_tip=set_status_tip,
            )
            self.minusBtn.clicked.connect(self.decrease)
            self.hboxlayout.addWidget(self.minusBtn)
        self.hboxlayout.addWidget(self.slider)
        if plus:
            self.plusBtn = self.initSliderBoxBtn(
                icon="widget/plus.svg", tip="increase slider value",
                accent_color=accent_color, where=where,
                set_status_tip=set_status_tip,
            )
            self.plusBtn.clicked.connect(self.increase)
            self.hboxlayout.addWidget(self.plusBtn)
        self.addSeparator()
        for btn in btns_list:
            self.hboxlayout.addWidget(btn)
        self.btns_list = btns_list
        self.hboxlayout.addStretch(1)
        # build widget vertical layout.
        self.setLayout(self.vboxlayout)
        self.vboxlayout.addWidget(self.sliderbox)
        self.slider.valueChanged.connect(self.updateFromSlider)
        self.readout.textChanged.connect(self.updateFromReadout)
        self.convertedValue = self.convertValue(value)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setSliderColor(self.accent_color)
        sliderColor = extractFromAccentColor(accent_color)
        print(f"sliderColor({sliderColor})")
        self.slider.setStyleSheet(
            FIGD_SLIDER_STYLE.render(
                SLIDER_COLOR=sliderColor,
            )
        )

    def addSeparator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #484848;''')
        sep.setLineWidth(1)
        self.hboxlayout.addWidget(sep)

    def setSliderColor(self, accent_color: str):
        grooveColor = accent_color
        if "qlineargradient" in accent_color or "qradialgradient" in accent_color or "qconicalgradient" in accent_color:
            grooveColor = accent_color.split(":")[-1].strip()
            grooveColor = grooveColor.split()[-1].split(")")[0]
            grooveColor = grooveColor.strip()    
        # reset palette.
        palette = self.slider.palette()
        palette.setColor(QPalette.Window, QColor(grooveColor))
        palette.setColor(QPalette.Button, QColor(grooveColor))
        palette.setColor(QPalette.Highlight, QColor(grooveColor))
        self.slider.setPalette(palette)

    def increase(self):
        value = self.slider.value()+1
        value = min(value, self.slider.maximum())
        self.slider.setValue(value)
        self.readout.setText(str(value))
        self.convertedValue = self.convertValue(value)

    def decrease(self):
        value = self.slider.value()-1
        value = max(value, self.slider.minimum())
        self.slider.setValue(value)
        self.readout.setText(str(value))
        self.convertedValue = self.convertValue(value)

    def setAccentColor(self, accent_color: str, where: str="back"):
        self.accent_color = accent_color
        # extract border color from the accent color.
        borderColor = extractFromAccentColor(
            accent_color, 
            where=where,
        )
        # stylesheet = """
        # QToolButton {
        #     font-size: 30px;
        #     border-radius: 2px;
        #     background: transparent;
        # }
        # QToolButton:hover {
        #     color: #292929;
        #     background: rgba(255, 255, 255, 0.5);
        #     /* background: """+accent_color+"""; */
        #     /* border: 1px solid """+borderColor+"""; */
        # }"""
        stylesheet = '''
        QToolButton {
            padding: 4px;
            border-radius: 5px; 
            font-family: Helvetica;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 0.5);
        }'''
        self.readout.setStyleSheet("""
        QLineEdit {
            padding: 0px;
            color: #929292;
            font-size: 16px;
            font-weight: bold;
            border-radius: 2px;
            background: #484848;
            selection-color: #292929;
            selection-background-color: """+self.accent_color+""";
        }""")
        if hasattr(self, "plusBtn"):
            self.plusBtn.setStyleSheet(stylesheet)
            self.plusBtn.setMaximumWidth(25)
            self.plusBtn.setMaximumHeight(25)
        if hasattr(self, "minusBtn"):
            self.minusBtn.setStyleSheet(stylesheet)
            self.minusBtn.setMaximumWidth(25)
            self.minusBtn.setMaximumHeight(25)
        self.setSliderColor(self.accent_color)

    def initSliderBoxBtn(self, text: str="", icon=None, tip: str="a tip",
                         accent_color: str="gray", where: str="back", 
                         set_status_tip: bool=True):
        btn = QToolButton()
        if icon: 
            btn.setIcon(FigD.Icon(icon))
        else: btn.setText(text)
        btn.setToolTip(tip)
        if set_status_tip:
            btn.setStatusTip(tip)
        btn.setIconSize(QSize(14,14))
        # set style sheet.
        stylesheet = '''
        QToolButton {
            padding: 4px;
            border-radius: 5px; 
            font-family: Helvetica;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 0.5);
        }'''
        btn.setStyleSheet(stylesheet)

        return btn

    def updateFromReadout(self):
        try: value = int(self.readout.text())
        except ValueError: return
        self.convertedValue = self.convertValue(value)
        self.slider.setValue(value)
        self.changed.emit(self.convertedValue)
        self.displayChanged.emit(value)
        self.updatedReadout.emit()

    def convertValue(self, value: int) -> float:
        """default conversion function. Redefine it for your custom slider.
        This functions purpose is to respect the difference in the scale of 
        values displayed in the UI and the scale of values needed by your 
        backend. E.g. opacity might be needed on a scale of 0-1 but the dev
        wants the user to pick on a scaled up integer percentage scale of 0 to 100.
        This function is responsible for that conversion from 0-100 to 0-1 for 
        the backend.

        Args:
            value (int): the value currently shown on the UI.

        Returns:
            float: the value needed by the backend.
        """
        return value

    def updateFromSlider(self, value: int):
        self.convertedValue = self.convertValue(value)
        self.changed.emit(self.convertedValue)
        self.readout.setText(str(value))
        self.displayChanged.emit(value)
        self.updatedSlider.emit()

# opacity slider
class FigDOpacitySlider(FigDSlider):
    def convertValue(self, value: int) -> float:
        value = max(min(value, 100), 0)
        value /= 100
        if hasattr(self, "window_ptr"):
            self.window_ptr.setWindowOpacity(value)

        return value

    def connectWindow(self, window: QMainWindow):
        self.window_ptr = window

# zoom slider
class FigDZoomSlider(FigDSlider):
    zoomChanged = pyqtSignal(float)
    def __init__(self, *args, **kwargs):
        super(FigDZoomSlider, self).__init__(*args, **kwargs)
        self.slider.sliderReleased.connect(self.emitZoomChanged)
        self.displayChanged.connect(self.emitZoomChanged2)

    def setValueOnTabChange(self, value: int):
        self.convertedValue = self.convertValue(value)
        self.readout.setText(str(self.convertedValue))
        self.slider.setValue(self.convertedValue)

    def emitZoomChanged2(self):
        value = self.slider.value()
        self.convertedValue = self.convertValue(value)        
        self.zoomChanged.emit(value)

    def emitZoomChanged(self):
        value = self.slider.value()
        self.convertedValue = self.convertValue(value)
        self.changed.emit(self.convertedValue)
        self.readout.setText(str(value))
        self.displayChanged.emit(value)
        self.updatedSlider.emit()
        self.zoomChanged.emit(value)

    def convertValue(self, value: int) -> float:
        value = min(max(value, 25), 250)

        return value

    def connectWindow(self, window: QMainWindow):
        self.window_ptr = window

# menu button for fig menu.
class FigDMenuButton(QWidget):
    """
    A widget to simulate the buttons of a QMenu by combining a toolbutton
    and a label. Sub menus are to be supported as well using instances of 
    QMenu. The label is used to display shortcuts.
    """
    def __init__(self, text: str, icon: str, tip: str="", 
                 accent_color: str="gray", icon_size: Tuple[int, int]=(20,20),
                 shortcut: Union[str, None]=None, parent: Union[None, QWidget]=None):
        super(FigDMenuButton, self).__init__(parent=parent)
        self.accent_color = accent_color
        self.__icon_size = QSize(*icon_size)
        self._submenu_shown = False
        # main horizontal layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(5)
        # QToolButton part of the context menu button.
        self._btn = QToolButton()
        self._btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        if icon != "": 
            self._btn.setIcon(FigD.Icon(icon))
            self._btn.setIconSize(self.__icon_size)
            self._btn.setText(" "+text)
        else:
            self._btn.setText("     "+text)
        if tip != "": 
            self._btn.setToolTip(tip)
            self._btn.setStatusTip(tip)
        # shortcut label.
        self.label = QLabel()
        self.label.setText(shortcut)
        # build button layout.
        self.hboxlayout.addWidget(self._btn)
        self.hboxlayout.addStretch(1)
        self.hboxlayout.addWidget(self.label)
        # wrapper.
        self.wrapper = QWidget()
        self.wrapper.setStyleSheet("background: transparent;")
        self.wrapper.setLayout(self.hboxlayout)
        self.wrapper.setObjectName("FigDMenuButton")
        # wrapper layout.
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.wrapper)
        # set layout.
        self.setLayout(layout)

    def setAccentColor(self, accent_color: str):
        self.accent_color = accent_color
        # style the sub menu if it exists.
        if hasattr(self, "contextMenu"):
            self.contextMenu = styleContextMenu(
                self.contextMenu, 
                self.accent_color
            )
        self.label.setStyleSheet("""
        QLabel {
            padding: 0px;
            color: #6e6e6e;
            background: transparent;
            font-size: 18px;
            font-family: "Be Vietnam Pro";
        }""")
        self._btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            padding: 3px;
            background: transparent;

            font-size: 18px;
            font-family: "Be Vietnam Pro";
        }""")
        self.wrapper.setStyleSheet("""
        QWidget#FigDMenuButton {
            color: #fff;
            padding: 3px;
            padding-left: 0px;
            border-radius: 5px;
            background: transparent;
            
            font-size: 18px;

            font-family: "Be Vietnam Pro";
        }
        QWidget#FigDMenuButton:hover {
            color: #292929;
            background-color: """+self.accent_color+""";
        }""")

    def setContextMenu(self, menu: QMenu):
        self.contextMenu = menu
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)

    def enterEvent(self, event):
        if hasattr(self, "contextMenu"):
            p = self.mapToGlobal(QPoint(0, 0))
            if not self._submenu_shown:
                self.contextMenu.popup(p)
            self._submenu_shown = True
        super(FigDMenuButton, self).enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "contextMenu"):
            self._submenu_shown = False
        super(FigDMenuButton, self).leaveEvent(event)

# settings menu for a FigDWindow type.
class FigDAppSettingsMenu(QMenu):
    def __init__(self, accent_color: str="gray", 
                 parent: Union[None, QWidget]=None,
                 tabs_enabled: bool=True):
        super(FigDAppSettingsMenu, self).__init__(parent)
        from fig_dash.ui.titlebar import FullScreenBtn
        self.sliders = []
        self.accent_color = accent_color
        # make the window transparent.
        if tabs_enabled: 
            self.addAction(
                FigD.Icon("tabbar/new-tab.png"), 
                "New tab", blank, QKeySequence("Ctrl+T")
            )
            self.addAction(
                "New window", blank, 
                QKeySequence("Ctrl+N")
            )
            self.addAction(
                "New Private window", blank, 
                QKeySequence("Ctrl+Shift+N")
            )
        self.addSeparator()
        self.addAction(FigD.Icon("textedit/history.svg"), "History")
        self.addAction(FigD.Icon("navbar/download.svg"), "Downloads", 
                       blank, QKeySequence("Ctrl+J"))
        self.bookmarksMenu = self.addMenu("Bookmarks")
        self.bookmarksMenu = styleContextMenu(
            self.bookmarksMenu,
            self.accent_color,
        )
        self.bookmarksMenu.addAction(
            "Bookmark this tab...", blank,
            QKeySequence("Ctrl+D"),
        )
        self.bookmarksMenu.addAction(
            "Bookmark all tabs...", blank,
            QKeySequence("Ctrl+Shift+D"),
        )
        self.bookmarksMenu.addSeparator()
        self.bookmarksMenu.addAction(
            "Show bookmarks", blank,
            QKeySequence("Ctrl+Shift+B"),
        )
        self.bookmarksMenu.addAction(
            "Bookmark manager", blank,
            QKeySequence("Ctrl+Shift+O"),
        )
        self.bookmarksMenu.addAction("Import bookmarks and settings...")
        self.bookmarksMenu.addSeparator()
        # self.bookmarksMenu.setVisible(True)
        self.addSeparator()
        self.opacitySlider = self.addSlider(
            "Opacity", class_=FigDOpacitySlider, 
            value=100, plus=True, minus=True,
            accent_color=accent_color,
        )
        self.fullscreenBtn = FullScreenBtn(
            fs_icon="titlebar/fullscreen.svg", 
            efs_icon="titlebar/exit_fullscreen.svg", 
            style="r", background=accent_color,
        )
        self.zoomSlider = self.addSlider(
            "Zoom     ", class_=FigDZoomSlider, 
            value=135, plus=True, minus=True, minm=25, 
            maxm=250, btns_list=[self.fullscreenBtn],
            accent_color=accent_color,
        )
        # self.opacitySlider.setFixedWidth(320)
        self.addSeparator()
        self.addAction(FigD.Icon("navbar/cast.svg"), "Cast tab")
        self.findInPage = self.addAction(
            FigD.Icon("titlebar/find_in_page.svg"), 
            "Find in page", blank, QKeySequence.Find,
        )
        self.findInPage.setVisible(False)
        # more tools menu.
        self.moreTools = self.addMenu("More tools ...")
        self.addSeparator()
        self.addToggle("Change theme", state1="Light", state2="Dark")
        self.addAction("Use system theme")
        self.addSeparator()
        self.notifsMenu = self.addMenu(
            FigD.Icon("menu/notifications.svg"), 
            "Notifications"
        )
        self.notifsMenu.addAction(
            "Mute", blank, 
            QKeySequence("Alt+Shift+M")
        )
        self.notifsMenu.addAction("Manage", blank)
        self.notifsMenu = styleContextMenu(self.notifsMenu, accent_color)
        self.addSeparator()
        self.addAction(
            FigD.Icon("navbar/permissions.svg"), 
            "Manage permissions"
        )
        self.addAction(
            FigD.Icon("navbar/more_settings.svg"), 
            "More settings ..."
        )
        self.addAction(FigD.Icon("help.svg"), "Help")
        self.addSeparator()
        self.addAction("Exit", QApplication.instance().quit)

    def connectWindow(self, window: QMainWindow):
        self.__window_ptr = window
        if window.bookmark_manager: pass
        if window.find_function:
            self.findInPage.setVisible(True)
            self.findInPage.triggered.connect(
                window.find_function
            )
        self.opacitySlider.connectWindow(self.__window_ptr)
        self.zoomSlider.connectWindow(self.__window_ptr)
        self.fullscreenBtn.setWindow(window)

    def addSlider(self, text: str="", class_=None, **kwargs):
        if class_:slider = class_(text=text, **kwargs)
        else: slider = FigDSlider(text=text, **kwargs)
        self.sliders.append(slider)
        widgetAction = QWidgetAction(self)
        widgetAction.setDefaultWidget(slider)
        self.addAction(widgetAction)
        
        return slider

    def addToggle(self, text: str="", 
                  state1: str="on", 
                  state2: str="off"):
        toggle = FigDToggle(
            text=text, state1=state1, 
            accent_color=self.accent_color,
            state2=state2,
        )
        # print(f"FigDToggle: {self.accent_color}")
        widgetAction = QWidgetAction(self)
        widgetAction.setDefaultWidget(toggle)
        self.addAction(widgetAction)

        return toggle

# dash widget simplified ribbon menu.
class DashWidgetSimplifiedRibbonMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashWidgetSimplifiedRibbonMenu, self).__init__(parent)

# Fig Dashboard app container class.
class FigDAppContainer(QApplication):
    def __init__(self, *args, **kwargs):
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        super(FigDAppContainer, self).__init__(*args, **kwargs)
        QFontDatabase.addApplicationFont(
            FigD.font("BeVietnamPro-Regular.ttf")
        )
        QFontDatabase.addApplicationFont(
            FigD.font("NotoSans-Medium.ttf")
        )
        self.active_window_ptr = None
        self._has_tray_icon = False
        # create tray menu.
        self.trayMenu = self.initTrayMenu()

    def createTrayIcon(self, tray_icon: str):
        # tray icon button.
        if self._has_tray_icon: return
        self.trayIcon = QSystemTrayIcon(FigD.Icon(tray_icon), self)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()
        self._has_tray_icon = True

    def initTrayMenu(self) -> QMenu:
        """create context menu for system tray icon.

        Returns:
            QMenu: context menu object.
        """
        # actions for tray icon context menu.
        self.showAllWindows = QAction("Show all windows")
        self.hideAllWindows = QAction("Hide all windows")
        self.quitApp = QAction("Quit application")
        self.openSettings = QAction("Open app settings")
        self.closeAll = QAction("Close all windows")
        # add icons.
        self.showAllWindows.setIcon(FigD.Icon("widget/show.svg"))
        self.hideAllWindows.setIcon(FigD.Icon("widget/hide.svg"))
        self.quitApp.setIcon(FigD.Icon("tray/close.svg"))
        self.closeAll.setIcon(FigD.Icon("tray/close.svg"))
        self.openSettings.setIcon(FigD.Icon("tray/settings.svg"))
        # connect functions to actions.
        self.closeAll.triggered.connect(self.closeAllWindows)
        self.showAllWindows.triggered.connect(self.show_all_windows)
        self.hideAllWindows.triggered.connect(self.hide_all_windows)
        self.quitApp.triggered.connect(self.quit)
        # tray icon menu.
        trayMenu = QMenu()
        # trayMenu.addAction(self.logsAction)
        # trayMenu.addAction(self.supportAction)
        # trayMenu.addSeparator()
        trayMenu.addAction(self.showAllWindows)
        trayMenu.addAction(self.hideAllWindows)
        trayMenu.addAction(self.closeAll)
        trayMenu.addSeparator()
        trayMenu.addAction(self.openSettings)
        trayMenu.addAction(self.quitApp)

        return trayMenu

    def hide_all_windows(self):
        for widget in self.topLevelWidgets():
            if isinstance(widget, FigDWindow):
                widget.hide()

    def show_all_windows(self):
        for widget in self.topLevelWidgets():
            if isinstance(widget, FigDWindow):
                widget.show()

    def show_active_window(self):
        window = QApplication.activeWindow()
        if window: window.show()

    def notify(self, obj, event):
        if isinstance(obj, FigDWindow) or (isinstance(obj, QMainWindow) and hasattr(obj, "deactivate") and hasattr(obj, "activate")):
            if event.type() == QEvent.WindowDeactivate:
                obj.titlebar.deactivate()
            if event.type() == QEvent.WindowActivate:
                obj.titlebar.activate()

        return super(FigDAppContainer, self).notify(obj, event)

# FigD tabwidget splitter button.
class FigDTabSplitBtn(QToolButton):
    def __init__(self, size: Tuple[int,int]=(20,20), 
                 accent_color: str="gray", alpha=150,
                 parent: Union[None, QWidget]=None):
        super(FigDTabSplitBtn, self).__init__(parent=parent)
        # accent color, bg alpha, border color.
        self.accent_color = accent_color
        self.border_color = extractFromAccentColor(accent_color)
        self.bg_alpha = setAccentColorAlpha(
            accent_color, 
            alpha=alpha,
        )
        self.setIcon(FigD.Icon("tabbar/split.svg"))
        self.setStyleSheet(jinja2.Template('''
        QToolButton {
            color: #fff;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
            border: 1px solid transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: {{ background }};
            border: 1px solid {{ border_color }};
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''').render(
                background=self.bg_alpha,
                border_color=self.border_color,
            )
        )
        self.setIconSize(QSize(*size))
        self.clicked.connect(self.showSplitterMenu)

    def showSplitterMenu(self):
        self.splitterMenu = QMenu()
        self.splitterMenu.addAction(FigD.Icon("tabbar/split-up.svg"), "Split Up")
        self.splitterMenu.addAction(FigD.Icon("tabbar/split-down.svg"), "Split Down")
        self.splitterMenu.addAction(FigD.Icon("tabbar/split-left.svg"), "Split Left")
        self.splitterMenu.addAction(FigD.Icon("tabbar/split-right.svg"), "Split Right")
        # style splitter menu.
        self.splitterMenu = styleContextMenu(
            self.splitterMenu, 
            self.accent_color,
        )
        # show splitter menu.
        pos = self.mapToGlobal(QPoint(0, 0))
        self.splitterMenu.popup(pos)

# FigD style tab corner widget class.
class FigDTabManager(QWidget):
    def __init__(self, accent_color: str="gray", 
                 parent: Union[None, QWidget]=None):
        super(FigDTabManager, self).__init__(parent=parent)
        self.setGraphicsEffect(self.createDropShadow(accent_color))
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(2)
        self.hboxlayout.setContentsMargins(0, 0, 5, 0)
        alpha = 150
        # accent color, bg alpha, border color.
        self.accent_color = accent_color
        self.border_color = extractFromAccentColor(accent_color)
        self.bg_alpha = setAccentColorAlpha(accent_color, alpha=alpha)
        # tab related buttons.
        self.splitterBtn = FigDTabSplitBtn(
            accent_color=accent_color, 
            size=(24,24), alpha=alpha,
        )
        self.deletedBtn = self.initCornerBtn("tabbar/trash.svg", size=(20,20))
        self.searchBtn = self.initCornerBtn("tabbar/search_tabs.svg", size=(20,20))
        # build layout.
        self.hboxlayout.addWidget(self.splitterBtn, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(self.deletedBtn, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(self.searchBtn, 0, Qt.AlignVCenter)
        # set layout and size policy.
        wrapper = QWidget()
        wrapper.setStyleSheet(f"""background: {FIGD_TABBAR_BACKGROUND};""")
        wrapper.setLayout(self.hboxlayout)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(wrapper, 0, Qt.AlignTop)
        wrapper.setFixedHeight(35)
        # set layout.
        self.setLayout(layout)

    def createDropShadow(self, accent_color: str="gray", 
                         where: str="back") -> QGraphicsDropShadowEffect:
        """create drop shadow from the accent color.
        Returns:
            QGraphicsDropShadowEffect: _description_
        """
        drop_shadow_color = extractFromAccentColor(accent_color, where)
        drop_shadow = QGraphicsDropShadowEffect()
        drop_shadow.setColor(QColor(drop_shadow_color))
        drop_shadow.setBlurRadius(50)
        drop_shadow.setOffset(0, 0)

        return drop_shadow

    def initCornerBtn(self, icon: str, size: Tuple[int,int]=(23,23)) -> QToolButton:
        btn = QToolButton()
        btn.setIcon(FigD.Icon(icon))
        btn.setStyleSheet(jinja2.Template('''
        QToolButton {
            color: #fff;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
            border: 1px solid transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: {{ background }};
            border: 1px solid {{ border_color }};
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''').render(
                background=self.bg_alpha,
                border_color=self.border_color,
            )
        )
        btn.setIconSize(QSize(*size))

        return btn

# tab controls.
class FigDTabControls(QWidget):
    def __init__(self, accent_color: str, 
                 parent: Union[None, QWidget]=None):
        super(FigDTabControls, self).__init__(parent=parent)
        # horizontal layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(5)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        # accent color.
        self.accent_color = accent_color
        # move, rename, duplicate, pin, share.
        self.hboxlayout.addStretch()
        self.hboxlayout.addStretch()
        self.reloadBtn = self.addBtn(FigD.Icon("tabbar/reload.svg"), tip="Reload")
        self.renameBtn = self.addBtn(FigD.Icon("tabbar/rename.svg"), tip="Rename")
        self.moveBtn = self.addBtn(FigD.Icon("tabbar/move.svg"), tip="Move to new window")
        self.duplicateBtn = self.addBtn(FigD.Icon("tabbar/duplicate.png"), tip="Duplicate")
        self.pinBtn = self.addBtn(FigD.Icon("tabbar/pin.svg"), tip="Pin")
        self.shareBtn = self.addBtn(FigD.Icon("tabbar/share.svg"), tip="Share")
        # set layout.
        self.setLayout(self.hboxlayout)

    def addBtn(self, icon: QIcon, tip="", func=None, 
               icon_size: Tuple[int,int]=(22,22)) -> QToolButton:
        btn = QToolButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(*icon_size))
        btn.setStyleSheet("""
        QToolButton {
            border: 0px;
            padding: 5px;
            border-radius: 5px;
            background: transparent;
        }
        QToolButton:hover {
            background: """+self.accent_color+""";
        }""")
        btn.setToolTip(tip)
        btn.setStatusTip(tip)
        count = self.hboxlayout.count()
        if func: btn.clicked.connect(func)
        self.hboxlayout.insertWidget(count-1, btn)

        return btn

# FigD style tab bar.
class FigDTabBar(QTabBar):
    def __init__(self, accent_color: str="gray", 
                 tabwidget: QTabWidget=None,
                 parent: Union[None, QWidget]=None):
        super(FigDTabBar, self).__init__(parent)
        self.setDrawBase(False)
        self.accent_color = accent_color
        self.border_color = extractFromAccentColor(accent_color)
        self.bg_alpha = setAccentColorAlpha(accent_color, alpha=150)
        self.tabwidget = tabwidget
        self.clicked_tab_index = -1
        # add new tab button.
        self.plusBtn = QToolButton(parent=self)
        self.plusBtn.setIcon(FigD.Icon("tabbar/new_tab.svg"))
        self.plusBtn.setStyleSheet(jinja2.Template('''
        QToolButton {
            color: #fff;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
            border: 1px solid transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: {{ background }};
            border: 1px solid {{ border_color }};
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''').render(
                background=self.bg_alpha,
                border_color=self.border_color,
            )
        )
        self.plusBtn.setIconSize(QSize(22,22))
        self.plusBtn.clicked.connect(self.openTab)
        self.setDrawBase(False)

    def initTabControls(self, menu: QMenu) -> QWidgetAction:
        # widget and layout.
        tabControls = FigDTabControls(
            accent_color=self.accent_color
        )
        self.reloadBtn = tabControls.reloadBtn
        self.renameBtn = tabControls.renameBtn
        self.moveBtn = tabControls.moveBtn
        self.duplicateBtn = tabControls.duplicateBtn
        self.pinBtn = tabControls.pinBtn
        self.shareBtn = tabControls.shareBtn
        # create widget action.
        widgetAction = QWidgetAction(menu)
        widgetAction.setDefaultWidget(tabControls)

        return widgetAction

    def openTab(self):
        self.tabwidget.openTab()

    def resizeEvent(self, event):
        super(FigDTabBar, self).resizeEvent(event)
        self.moveNewTabBtn()

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QTabBar.sizeHint(self) 
        width = sizeHint.width()
        height = sizeHint.height()
        return QSize(width+25, height)

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the new tab button is in the correct location.
        """
        super(FigDTabBar, self).tabLayoutChange()
        self.moveNewTabBtn()

    def moveNewTabBtn(self):
        self.setDrawBase(False)
        size = sum(self.tabRect(i).width() for i in range(self.count()))
        # Set the new tab button location in a visible area
        y = 4 # y = self.geometry().top()+4
        if size > self.width():
            x = self.width()-54
        else: x = size
        x = x+5
        # print("ui::FigDTabBar.moveNewTabBtn:", x, y)
        # Show just to the left of the scroll buttons
        self.plusBtn.move(x, y)

    def initTabMenu(self) -> QMenu:
        contextMenu = QMenu()
        # tab controls: move, rename, duplicate, pin, share
        tabControls = self.initTabControls(self)
        contextMenu.addAction(tabControls)
        # if new tab requested (True signifies towards the right.)
        self._cmenu_new_tab_to_left = contextMenu.addAction(
            "New tab to left", 
            self.addTabToTheLeft
        )
        self._cmenu_new_tab_to_right = contextMenu.addAction(
            "New tab to right", 
            self.addTabToTheRight
        )
        contextMenu.addSeparator()
        contextMenu.addAction(
            FigD.Icon("tabbar/reading_list.svg"), 
            "Add tab to reading list"
        )
        contextMenu.addAction("Add tab to group")
        contextMenu.addSeparator()
        self._split_submenu = contextMenu.addMenu(FigD.Icon("tabbar/split.svg"), "Split")
        self._split_submenu = styleContextMenu(self._split_submenu, self.accent_color)
        self._split_submenu.addAction(FigD.Icon("tabbar/split-up.svg"), "Split Up")
        self._split_submenu.addAction(FigD.Icon("tabbar/split-down.svg"), "Split Down")
        self._split_submenu.addAction(FigD.Icon("tabbar/split-left.svg"), "Split Left")
        self._split_submenu.addAction(FigD.Icon("tabbar/split-right.svg"), "Split Right")

        return contextMenu

    def initTabBarMenu(self) -> QMenu:
        contextMenu = QMenu()
        contextMenu.addAction("Minimize")
        contextMenu.addAction("Maximize")
        contextMenu.addSeparator()
        self._cmenu_new_tab = contextMenu.addAction(
            FigD.Icon("tabbar/new-tab.png"), 
            "New tab", blank, QKeySequence("Ctrl+T")
        )
        self._cmenu_reopen_closed_tab = contextMenu.addAction(
            "Reopen closed tab", blank, 
            QKeySequence("Ctrl+Shift+T")
        )
        self._cmenu_save_tab_list = contextMenu.addAction(
            FigD.Icon("tabbar/save-tab-list.png"), 
            "Bookmark all tabs...", blank, 
            QKeySequence("Ctrl+Shift+D")
        )
        contextMenu.addSeparator()
        self._cmenu_open_task_manager = contextMenu.addAction(
            "Task Manager", blank, 
            QKeySequence("Shift+Esc")
        )
        contextMenu.addSeparator()
        self._cmenu_close = contextMenu.addAction(
            "Close", blank, 
            QKeySequence("Ctrl+Shift+W")
        )

        return contextMenu

    def addTabToTheLeft(self):
        if self.clicked_tab_index != -1:
            self.tabwidget.openTabAt(self.clicked_tab_index)

    def addTabToTheRight(self):
        if self.clicked_tab_index != -1:
            self.tabwidget.openTabAt(self.clicked_tab_index+1)

    def getClickedTabIndex(self, pos) -> int:
        """compute tab number of clicked tab.
        Returns:
            int: index of the clicked tab.
        """
        count = self.count()
        clickedItem: int = -1
        for i in range(count):
            if self.tabRect(i).contains(pos):
                clickedItem = i
                break

        return clickedItem

    def contextMenuEvent(self, event):
        pos = event.pos()
        print(pos)
        # compute the tab number.
        i = self.getClickedTabIndex(pos)
        self.clicked_tab_index = i
        # Fig style context menu
        if i == -1:
            self.contextMenu = self.initTabBarMenu()
        else:
            self.contextMenu = self.initTabMenu()
            self.contextMenu.addSeparator()
            self.contextMenu.addAction(
                FigD.Icon("tabbar/close.png"), "Close", 
                partial(self.tabwidget.removeTab, i), 
                QKeySequence.Close
            )
            self.contextMenu.addAction(
                FigD.Icon("tabbar/close-all.png"), "Close other tabs", 
                partial(self.tabwidget.removeComplement, i)
            )
            self.contextMenu.addAction(
                FigD.Icon("tabbar/close-left.png"), 
                "Close tabs to left", 
                partial(self.tabwidget.removeLeft, i),
            )
            self.contextMenu.addAction(
                FigD.Icon("tabbar/close-right.png"), 
                "Close tabs to right",
                partial(self.tabwidget.removeRight, i),
            )
            self.contextMenu.addSeparator()
            self.contextMenu.addAction(FigD.Icon("tabbar/mute.svg"), "Mute site")
            self.contextMenu.addAction(FigD.Icon("tabbar/devices.svg"), "Send to device")
        # launch context menu and style it.
        self.contextMenu = styleContextMenu(
            self.contextMenu, 
            self.accent_color,
            icon_size=30,
        )
        self.contextMenu.popup(event.globalPos())
        # if action == renameTab:
        #     # print(event.x(), event.y())
        #     try: self.tabs.renameDialog(clickedItem)
        #     except Exception as e: 
        #         print("\x1b[31;1mtab.contextMenuEvent\x1b[0m", e)
        # elif action == moveTab:
        #     app = QApplication.instance()
        #     currentWidget = self.tabs.currentWidget()
        #     url = currentWidget.browser.url()
        #     window = app.newMainWindow(url=url)
        #     window.show()

# FigD style tabwidget class.
class FigDTabCtrlBtn(QToolButton):
    """tab control buttons."""
    def __init__(self, icon, active_icon=None,
                 size: Tuple[int,int]=(18,18),
                 parent: Union[QWidget, None]=None,
                 tabwidget: Union[QTabWidget, None]=None):
        super(FigDTabCtrlBtn, self).__init__(parent)
        self.tabwidget = tabwidget
        self.clickedIndex = -1
        self.icon_path = icon
        if active_icon:
            self.active_icon_path = active_icon
        else: self.active_icon_path = self.icon_path
        self.setIcon(FigD.Icon(self.icon_path))
        self.setIconSize(QSize(*size))

    def connect(self, func):
        self.func = func
        self.clicked.connect(self.response)

    def response(self):
        clickedIndex = self.getTabIndex()
        print(self.tabwidget.tabBar().tabData(clickedIndex))
        print(f"response for tab-{clickedIndex}")
        if clickedIndex != -1:
            self.func(clickedIndex)

    def getTabIndex(self) -> int:
        """compute index of the tab the control button is attached to.
        Returns:
            int: index of tab the control button belongs to.
        """
        if self.tabwidget is None: return -1
        # map top left corner to coordinate space of FigDTabBar
        # parent of TabCtrlBtn is tabButton.
        # map to parent on tabButton maps to it's parent which is FigDTabBar.
        topLeft = self.parent().mapToParent(
            self.rect().topLeft()
        )
        w = self.rect().width()
        h = self.rect().height()
        # create translated rectangle (coordinate space of FigDTabBar) of control button.
        transRect = QRect(topLeft.x(), topLeft.y(), w, h)
        # get index of tab to which control button belongs to.
        tabBar = self.tabwidget.tabBar()
        for i in range(tabBar.count()):
            print("tabBarRect:", tabBar.tabRect(i))
            if tabBar.tabRect(i).contains(transRect): 
                return i

        return -1

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon_path))
        super(FigDTabCtrlBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.icon_path))
        super(FigDTabCtrlBtn, self).leaveEvent(event)

# FigD tabbar settings button.
class FigDTabSettingsBtn(QWidget):
    def __init__(self, accent_color: str="gray", 
                 where: str="back", tabwidget=None,
                 parent: Union[None, QWidget]=None):
        super(FigDTabSettingsBtn, self).__init__(parent=parent)
        self.tabwidget = tabwidget
        self.accent_color = accent_color
        self.border_color = extractFromAccentColor(accent_color, where)
        self.bg_alpha = setAccentColorAlpha(accent_color)
        # settings btn.
        btn = QToolButton()
        btn.setIcon(FigD.Icon("tabbar/settings.png"))
        btn.setStyleSheet(jinja2.Template('''
        QToolButton {
            color: #fff;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
            border: 1px solid transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: {{ background }};
            border: 1px solid {{ border_color }};
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''').render(
                background=self.bg_alpha,
                border_color=self.border_color,
            )
        )
        blank = QWidget()
        blank.setFixedWidth(5)
        btn.setIconSize(QSize(22,22))
        # wrapper for ..
        wrapper = QWidget()
        wrapper.setStyleSheet(f"""background: {FIGD_TABBAR_BACKGROUND};""")
        wrapper.setFixedHeight(35)
        # vboxlayout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.addWidget(btn, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(blank, 0, Qt.AlignVCenter)
        # set vboxlayout to wrapper.
        wrapper.setLayout(self.hboxlayout)
        # wrapper layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(wrapper, 0, Qt.AlignTop)
        # set layout.
        self.setLayout(layout)
        btn.clicked.connect(self.showSettingsMenu)

    def showSettingsMenu(self):
        self.contextMenu = QMenu()
        if self.tabwidget:
            if self.tabwidget.tabPosition() != QTabWidget.North:
                self.contextMenu.addAction(
                    "Horizontal tabbar at top",
                    self.tabwidget.setNorth,
                )
            if self.tabwidget.tabPosition() != QTabWidget.South:
                self.contextMenu.addAction(
                    "Horizontal tabbar at bottom",
                    self.tabwidget.setSouth,
                )
            if self.tabwidget.tabPosition() != QTabWidget.West:
                self.contextMenu.addAction(
                    "Vertical tabbar at left",
                    partial(self.tabwidget.setTabPosition, QTabWidget.West),
                )
            if self.tabwidget.tabPosition() != QTabWidget.East:
                self.contextMenu.addAction(
                    "Vertical tabbar at right",
                    partial(self.tabwidget.setTabPosition, QTabWidget.East),
                )
        self.contextMenu.addAction("Tabs from other devices")
        pos = self.mapToGlobal(QPoint(0, 0))
        self.contextMenu = styleContextMenu(
            self.contextMenu, 
            self.accent_color,
        )
        self.contextMenu.popup(pos)

FIGD_TABWIDGET_STYLE = r"""
QTabWidget {
    color: #fff;
    border: none;
    font-family: 'Be Vietnam Pro';
    background: transparent;
}
QTabWidget::pane {
    border: none;
    background: transparent;
}
QTabWidget::right-corner {
    border: none;
}
QTabBar {
    border: none;
    qproperty-drawBase: 0;
    background: """+FIGD_TABBAR_BACKGROUND+r""";
}
QTabBar::close-button {
    background: url("/home/atharva/GUI/fig-dash/resources/icons/close.png");
    background-repeat: no-repeat;
    background-position: center;
}
QTabBar::close-button:hover {
    background: url("/home/atharva/GUI/fig-dash/resources/icons/close-active.png");
    background-repeat: no-repeat;
    background-position: center;
}
QTabBar::tab {
    border: none;
    color: #fff;

    margin-left: 0px;
    margin-right: 0px;

    padding-top: 4px;
    padding-left: 9px;
    padding-right: 5px;
    padding-bottom: 4px;

    font-size: 17px;
    font-family: 'Be Vietnam Pro', sans-serif;
    max-width: 300px;
    background: rgba(0, 0, 0, 0.8);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}
QTabBar::tab:hover {
    color: #fff;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    background: rgba(50, 50, 50, 0.8);
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 200), stop : 0.3 rgba(191, 54, 54, 220), stop : 0.6 rgba(235, 95, 52, 220), stop: 0.9 rgba(235, 204, 52, 220)); */
}
QTabBar::tab:selected {
    color: #eee;
    border: none;
    font-weight: bold;
    
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    background: rgba(80, 80, 80, 0.8);
    background-image: url(/home/atharva/GUI/fig-dash/resources/icons/textedit/NoiseGaussBlur(5).png);
    
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e4852c, stop : 0.143 #e4822d, stop : 0.286 #e4802f, stop : 0.429 #e47d30, stop : 0.571 #e47b32, stop : 0.714 #e47833, stop : 0.857 #e47635, stop : 1.0 #e47336); background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
    

    padding-top: 4px;
    padding-left: 9px;
    padding-right: 5px;
    padding-bottom: 4px;
    
    margin-left: 0px;
    margin-right: 0px;
    
    font-size: 17px;
    font-weight: bold;
}"""
FIGD_TABWIDGET_CTRL_BTN_ACTIVE_STYLE = jinja2.Template(r"""
QToolButton {
    color: #fff;
    font-size: 14px;
    border-radius: 2px;
    background: transparent;
    border: 1px solid transparent;
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}""")
FIGD_TABWIDGET_CTRL_BTN_STYLE = jinja2.Template(r"""
QToolButton {
    color: #fff;
    font-size: 14px;
    border-radius: 2px;
    background: transparent;
    border: 1px solid transparent;
}
QToolButton:hover {
    color: #292929;
    background: {{ background }};
    border: 1px solid {{ border_color }};
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}""")
# tab widget for FigD.
class FigDTabWidget(QTabWidget):
    zoomChanged = pyqtSignal(int)
    showMessage = pyqtSignal(str)
    changeWindowTitle = pyqtSignal(str)
    def __init__(self, widget_factory=None, window_factory=None, 
                 parent: Union[None, QWidget]=None, tab_icon: str="",
                 tab_title: str="New tab", widget_args={}, window_args={},
                 accent_color: str="gray", autohide: bool=True, where: str="back"):
        super(FigDTabWidget, self).__init__(parent)
        # tab icon and title for new tabs.
        self.tab_icon = FigD.Icon(tab_icon)
        self.tab_title = tab_title
        # window and widget factories and arguments.
        self.window_factory = window_factory
        self.widget_factory = widget_factory
        self.window_args = window_args
        self.widget_args = widget_args 
        # drop shadow.
        drop_shadow = self.createDropShadow(
            accent_color, where
        )
        self.accent_color = accent_color        
        self.border_color = extractFromAccentColor(accent_color)
        self.bg_alpha = setAccentColorAlpha(accent_color, alpha=150)
        # set style sheet.
        self.resetCornerWidgets()
        self.tab_bar = FigDTabBar(
            accent_color=accent_color,
            tabwidget=self,
        )
        # set stuff.
        self.setTabBar(self.tab_bar)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setDocumentMode(True)
        self.setTabBarAutoHide(autohide)
        self.setElideMode(Qt.ElideRight)
        self.setObjectName("FigDTabWidget") # set object name.
        self.setStyleSheet(FIGD_TABWIDGET_STYLE) # set stylesheet.
        self.tab_bar.setGraphicsEffect(drop_shadow)
        self.tab_bar.setDrawBase(False)
        # connect slots to signals.
        self.currentChanged.connect(self.onTabChange)
        self.tabCloseRequested.connect(self.closeRequestedTab)
        # shortcuts
        self.AddTab = FigDShortcut(QKeySequence.AddTab, self, "Open new tab")
        self.AddTab.connect(self.openTab)
        self.NewWindow = FigDShortcut(QKeySequence.New, self, "Open new window")
        self.NewWindow.connect(self.openWindow)
        self.CloseTab = FigDShortcut(QKeySequence.Close, self, "Close tab/window")
        self.CloseTab.connect(self.closeCurrentTab)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def resetCornerWidgets(self, loc=Qt.TopLeftCorner, loc1=Qt.TopRightCorner):
        print(f"\x1b[34;1mui::FigDTabWidget.resetCornerWidgets({loc}, {loc1})\x1b[0m")
        tab_manager1 = FigDTabManager(
            accent_color=self.accent_color,
        )
        tab_manager2 = FigDTabManager(
            accent_color=self.accent_color,
        )
        tab_settings1 = FigDTabSettingsBtn(
            accent_color=self.accent_color,
            tabwidget=self,
        )
        tab_settings2 = FigDTabSettingsBtn(
            accent_color=self.accent_color,
            tabwidget=self,
        )
        self.setCornerWidget(tab_settings1, Qt.TopLeftCorner)
        self.setCornerWidget(tab_settings2, Qt.BottomLeftCorner)
        self.setCornerWidget(tab_manager1, Qt.TopRightCorner)
        self.setCornerWidget(tab_manager2, Qt.BottomRightCorner)

    def setSouth(self):
        self.setTabPosition(QTabWidget.South)
        self.resetCornerWidgets(
            Qt.BottomLeftCorner, 
            Qt.BottomRightCorner,
        )
        self.tabBar().moveNewTabBtn()

    def setNorth(self):
        self.setTabPosition(QTabWidget.North)
        self.resetCornerWidgets()
        self.tabBar().moveNewTabBtn()

    def showEvent(self, event):
        """if you want to modify show event"""
        super(FigDTabWidget, self).showEvent(event)

    def createDropShadow(self, accent_color, where):
        drop_shadow_color = extractFromAccentColor(
            accent_color, where=where
        )
        drop_shadow = QGraphicsDropShadowEffect()
        drop_shadow.setColor(QColor(drop_shadow_color))
        drop_shadow.setBlurRadius(50)
        drop_shadow.setOffset(0, 0)

        return drop_shadow

    def onCurrentWidget(self, func: str="", args: list=[], kwargs: dict={}):
        if func == "": return
        widget = self.currentWidget()
        obj = widget
        for attr in func.split("."):
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
            else: return
        obj(*args, **kwargs)

    def onTabChange(self):
        widget = self.currentWidget()
        if hasattr(widget, "getWindowTitle"):
            windowTitle = widget.getWindowTitle()
            self.changeWindowTitle.emit(windowTitle)
        if hasattr(widget, "browser") and hasattr(widget.browser, "zoomFactor"):
            print("switched tab has zoom:", int(100*widget.browser.zoomFactor()))
            self.zoomChanged.emit(
                int(100*widget.browser.zoomFactor())
            )
        elif hasattr(widget, "webview") and hasattr(widget.webview, "zoomFactor"):
            print("switched tab has zoom:", int(100*widget.webview.zoomFactor()))
            self.zoomChanged.emit(
                int(100*widget.webview.zoomFactor())
            )
        # if hasattr(widget, "signalZoom"):
        #     widget.signalZoom()
    def connectTitleBar(self, titlebar):
        self.titlebar = titlebar

    def closeCurrentTab(self):
        i = self.currentIndex()
        if i == 0: 
            QApplication.activeWindow().close()
        else: self.removeTab(i)

    def closeRequestedTab(self, i: int):
        self.removeTab(i)
        if len(self) == 0:
            QApplication.activeWindow().close()

    def changeCurrentTabTitle(self, title: str):
        i = self.currentIndex() # print(title)
        self.setTabText(i, title)

    def changeCurrentTabIcon(self, icon: str):
        print(f"\x1b[33;mchanging tab icon: {icon}\x1b[0m")
        i = self.currentIndex() # print("\x1b[31;1mui::__init__::FigDTabWidget.changeCurrentTabIcon:\x1b[0m", icon)
        self.setTabIcon(i, QIcon(icon))

    def wrapWidget(self, widget: QWidget, titlebar: Union[WindowTitleBar, None]=None) -> QWidget:
        # connects slots to optionally defined widget signals.
        if hasattr(widget, "changeTabTitle"):
            print("\x1b[33mconnected to changeTabTitle\x1b[0m")
            widget.changeTabTitle.connect(self.changeCurrentTabTitle)
        if hasattr(widget, "changeTabIcon"):
            print("\x1b[33mconnected to changeTabIcon\x1b[0m")
            widget.changeTabIcon.connect(self.changeCurrentTabIcon)
        if hasattr(widget, "changeTabToolTip"):
            print("\x1b[33mconnected to changeTabToolTip\x1b[0m")
            widget.changeTabToolTip.connect(self.changeCurrentTabToolTip)
        if hasattr(widget, "changeWindowTitle") and titlebar:
            print("\x1b[33mconnected to changeWindowTitle\x1b[0m")
            widget.changeWindowTitle.connect(titlebar.setTitle)
        if hasattr(widget, "zoomChanged") and titlebar:
            widget.zoomChanged.connect(titlebar.zoomSlider.setZoomValue)
        if hasattr(widget, "showMessage"):
            print("\x1b[33mconnected to showMessage\x1b[0m")
            widget.showMessage.connect(self.emitStatusBarMessage)

        return widget

    def emitStatusBarMessage(self, msg: str):
        """forward any messages recieved from the widget to the window."""
        self.showMessage.emit(msg)

    def widgetFactory(self) -> QWidget:
        """factory function for intialization of the widget
        type which is being tabbed."""
        if self.widget_factory is None: 
            raise NotImplementedError("`widget_factory` method not implemented.")
        widget = self.widget_factory(**self.widget_args)
        # connects slots to optionally defined widget signals.
        titlebar = None
        if hasattr(self, "titlebar"):
            titlebar = self.titlebar
        widget = self.wrapWidget(widget, titlebar)

        return widget 

    def tabFactory(self, widget: QWidget, index=None):
        """create tab from widget and index value."""
        if index is None:
            i = self.addTab(
                widget, self.tab_icon, 
                self.tab_title
            )
        else: 
            i = self.insertTab(
                index, widget, 
                self.tab_icon, 
                self.tab_title,
            )
        tabCtrlBtns = self.initTabCtrlBtns()
        pinAndGroup = self.initPinAndGroup()
        # tab control button close and mute slots.
        tabCtrlBtns.muteBtn.connect(self.muteTab)
        tabCtrlBtns.closeBtn.connect(self.tabCloseRequested.emit)
        self.tabBar().setTabButton(i, QTabBar.LeftSide, pinAndGroup)
        self.tabBar().setTabButton(i, QTabBar.RightSide, tabCtrlBtns)
        self.tabBar().setTabData(i, QVariant({
            "muted": False,
            "pinned": False,
            "creationIndex": i,
            "lastIndex": i, 
            "lastText": self.tab_title, 
            "lastIcon": self.tab_icon,
            "isGroupHead": False, 
            "groupName": None,
        }))
        # web page to be returned. (required by createWindow, to create new tab).
        # NOTE: the webview/browser instance associated with any widget is contained inside the 
        # .browser or .webview attribute otherwise `None` is returned as the value of the loaded page.
        page = None
        if hasattr(widget, "webview"):
            page = widget.webview.page()
        if hasattr(widget, "browser"):
            page = widget.browser.page()

        return i, page

    def openTabAt(self, i):
        widget = self.widgetFactory()
        j, page = self.tabFactory(widget, i)
        self.setCurrentIndex(j)

        return page

    def muteTab(self, i: int):
        print(f"ui::__init__::FigDTabWidget.muteTab({i})")

    def openTab(self):
        widget = self.widgetFactory()
        i, page = self.tabFactory(widget)
        self.setCurrentIndex(i)

        return page

    def changeCurrentTabToolTip(self, tabToolTip: str):
        i = self.currentIndex()
        self.setTabToolTip(i, tabToolTip)

    def initGroupName(self, color: str="orange",
                      placeHolder: str="New") -> QLineEdit:
        groupName = QLineEdit()
        groupName.setStyleSheet("""
        QLineEdit {
            color: #292929;
            font-size: 17px;
            background: """+color+""";
            border-radius: 5px;
        }""")
        groupName.setText(placeHolder)
        groupName.setReadOnly(True)
        groupName.setFixedHeight(25)
        groupName.setFixedWidth(40)

        return groupName

    def initPinAndGroup(self) -> QWidget:
        """create container having group name label and pinned tab button.
        Returns:
            QWidget: container with group and pin button.
        """
        # create container and it's layout.
        container = QWidget()
        container.setSizePolicy(
            QSizePolicy.Minimum, 
            QSizePolicy.Minimum,
        )
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        # create group and pin button.
        groupName = self.initGroupName()
        pinBtn = QToolButton()
        pinBtn.setIcon(FigD.Icon("tabbar/pin.svg"))
        pinBtn.setStyleSheet(
            FIGD_TABWIDGET_CTRL_BTN_STYLE.render(
                background=self.bg_alpha,
                border_color=self.border_color,
            )
        )
        pinBtn.hide()
        groupName.hide()
        # build layout.
        layout.addWidget(groupName)
        layout.addWidget(pinBtn)
        container.setStyleSheet("""
        QWidget {
            color: #fff;
            background: transparent;
        }""")

        return container

    def initTabCtrlBtns(self) -> QWidget:
        ctrlBtns = QWidget()
        ctrlLayout = QHBoxLayout()
        ctrlLayout.setSpacing(0)
        ctrlLayout.setContentsMargins(0, 0, 0, 0)
        ctrlBtns.setLayout(ctrlLayout)
        # mute & close button.
        muteBtn = self.initTabCtrlBtn("tabbar/mute.svg")
        closeBtn = self.initTabCtrlBtn(
            "close.png", 
            "close-active.png",
            size=(24,24),
        )
        muteBtn.hide()
        ctrlBtns.muteBtn = muteBtn
        ctrlBtns.closeBtn = closeBtn
        ctrlLayout.addWidget(muteBtn)
        ctrlLayout.addWidget(closeBtn)

        return ctrlBtns

    def initTabCtrlBtn(self, icon, active_icon=None, 
                       size: Tuple[int,int]=(18,18)) -> QToolButton:
        """tab control buttons."""
        btn = FigDTabCtrlBtn(
            icon, active_icon, size,
            tabwidget=self,
        )
        if active_icon:
            btn.setStyleSheet(
                FIGD_TABWIDGET_CTRL_BTN_ACTIVE_STYLE.render(
                    background=self.bg_alpha,
                    border_color=self.border_color,
                )
            )
        else:
            btn.setStyleSheet(
                FIGD_TABWIDGET_CTRL_BTN_STYLE.render(
                    background=self.bg_alpha,
                    border_color=self.border_color,
                )
            )

        return btn

    def removeLeft(self, i: int):
        """
        remove all tabs to the left of the ith one, excluding the ith one.
        Assuming indexing starts at 0.
        """
        for ind in range(i):
            self.removeTab(0)

    def removeRight(self, i: int):
        """
        remove all tabs to the right of the ith one, excluding the ith one.
        Assuming indexing starts at 0.
        """
        for ind in range(i+1, len(self)):
            self.removeTab(i+1)

    def removeComplement(self, i: int):
        """remove all tabs except the ith one, i.e:
        1) Remove all tabs to the left of the ith one.
        2) Remove all tabs to the right of the 0th one.
        """
        # remove all the tabs to the left of the ith one.
        self.removeLeft(i)
        # after removing all the tabs to the left, the ith one becomes the 0th tab
        # now remove all the tabs to the right of the 0th (originally the ith) one
        self.removeRight(0)

    def openWindow(self):
        if self.window_factory is None: return
        window = self.window_factory(**self.window_args)
        window.show()

        return window

    def changeZoom(self, zoomValue: float):
        """React to change in zoom value of the zoom slider.
        Args:
            zoomValue (float): the zoom value
        """
        if hasattr(self.currentWidget(), "changeZoom"):
            # print(f"{self.currentWidget()}.changeZoom({zoomValue})")
            self.currentWidget().changeZoom(zoomValue)

# search and navigation bar.
IMAGE_SEARCH_ICON_TEMPLATE = jinja2.Template(r"""
<svg focusable="false" height="24px" preserveaspectratio="xMidYMid meet" style="pointer-events: none; display: block; width: 100%; height: 100%;" version="1.1" viewbox="0 0 24 24" width="24px" xmlns="http://www.w3.org/2000/svg">
 <g>
  <circle fill="{{ ACCENT_COLOR }}" cx="12" cy="12" r="3.2">
  </circle>
  <path fill="{{ ACCENT_COLOR }}" d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z">
  </path>
 </g>
</svg>""")
class FigDSearchBar(QLineEdit):
	def __init__(self, accent_color: str="gray", 
                 placeholder_text: str="Search",
				 parent: Union[QWidget, None]=None):
		super(FigDSearchBar, self).__init__(parent)
		self.accent_color = accent_color
        # create actions.
		self.action_slots = {}
		self.action_icon_templates = {}
		self.action_icon_templates["imageSearch"] = IMAGE_SEARCH_ICON_TEMPLATE
		self.voiceSearch = self.addAction(
			FigD.Icon("lineedit/mic.svg"),
			QLineEdit.TrailingPosition
		)
		self.imageSearch = self.addAction(
            QIcon(FigD.createTempPath(
                IMAGE_SEARCH_ICON_TEMPLATE.render(
                    ACCENT_COLOR="#949494",
                ), ext="svg"
            )),
            QLineEdit.TrailingPosition,
        )
		self.imageSearch.setCheckable(True)
		self.imageSearch.setChecked(False)
		self.translate = self.addAction(
            FigD.Icon("lineedit/trans.svg"), 
            QLineEdit.TrailingPosition
        )
		self.bookmark = self.addAction(
			FigD.Icon("lineedit/bookmark.svg"),
			QLineEdit.TrailingPosition	
		)
		self.toggleCase = self.addAction(
            FigD.Icon("lineedit/case.svg"), 
            QLineEdit.TrailingPosition
        )
		self.searchAction = self.addAction(
            FigD.Icon("lineedit/image_search.svg"), 
            QLineEdit.LeadingPosition
		)
		self._search_lang = "en"
		# respond to triggering of actions.
		self.toggleCase.triggered.connect(self.toggleCaseSensitivity)
		self.setStyleSheet("""
        QLineEdit {
            color: #fff;
            padding: 5px;
            font-size: 17px;
            background: #292929;
            border-radius: 5px;
            selection-color: #292929;
            selection-background-color: """+self.accent_color+""";
            font-family: "Be Vietnam Pro";
        }""")
		self.setClearButtonEnabled(True)
		self.setPlaceholderText(placeholder_text)
		self.history = []
		# completer.
		self.qcompleter = QCompleter()
		# model.
		self.qcompleter.popup().setStyleSheet("""
        QWidget {
            color: #949494;
            background: #292929;
            selection-color: #292929;
            selection-background-color: """+self.accent_color+""";
            font-family: "Be Vietnam Pro";
        }""")
		self.stringModel = QStringListModel(self.history)
		# set model for completer.
		self.qcompleter.setModel(self.stringModel)
		# set completer.
		self.setCompleter(self.qcompleter)
		self.setMinimumWidth(600)

	def connect(self, action: str, slot):
		self.action_slots[action] = slot
		getattr(self, action).triggered.connect(
            partial(self.trigger, action)
        )

	def trigger(self, text: str):
		print(f"triggered {text}")
		action: QAction = getattr(self, text)
		if action.isChecked():
			if text in self.action_icon_templates:
				accent_color = extractFromAccentColor(self.accent_color)
		else: # print(f"accent_color: {self.accent_color}") 
			if text in self.action_icon_templates:
				accent_color = "#949494"
		rendered = self.action_icon_templates[text].render(
			ACCENT_COLOR=accent_color,
		)
		action.setIcon(QIcon(
			FigD.createTempPath(rendered, ext="svg")
		))
		self.action_slots[text]()		

	def lang(self):
		return self._search_lang

	def contextMenuEvent(self, event):
		self.contextMenu = self.createStandardContextMenu()
		self.contextMenu = styleContextMenu(
			self.contextMenu, 
			self.accent_color,
		)
		self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
		self.contextMenu.popup(event.globalPos())

	def toggleCaseSensitivity(self):
		if self.qcompleter.caseSensitivity() == Qt.CaseSensitive:
			print("case insensitive")
			self.qcompleter.setCaseSensitivity(Qt.CaseInsensitive)
		else: 
			print("case sensitive")
			self.qcompleter.setCaseSensitivity(Qt.CaseSensitive)

	def append(self, url_or_path: Union[str, QUrl]):
		if isinstance(url_or_path, QUrl):
			url_or_path = url_or_path.toString()
		self.history.append(url_or_path)
		self.stringModel = QStringListModel(self.history)
		self.qcompleter.setModel(self.stringModel)
		self.setCompleter(self.qcompleter)

# FigD window navigation bar button.
class FigDNavBtn(QToolButton):
    def __init__(self, role: str="back", home_url="", accent_color: str="gray", 
                 enabled: bool=False, max_items: int=20, parent: Union[None, QWidget]=None):
        super(FigDNavBtn, self).__init__(parent)
        self.role = role
        self.browser = None
        self.home_url = home_url
        self.max_items = max_items
        self._is_enabled = enabled
        self.accent_color = accent_color
        # icon paths.
        self.hover_icon_path = ""
        self.disabled_icon_path = ""
        self.history_items = []
        # connect slot according to role.
        if role == "back":
            self.icon_path = "textedit/back_disabled.svg"
            self.clicked.connect(self.back)
        elif role == "forward":
            self.icon_path = "textedit/forward_disabled.svg"
            self.clicked.connect(self.forward)
        elif role == "reload":
            self.icon_path = "textedit/reload.svg"
            self.clicked.connect(self._reload)
        elif role == "home":
            self.icon_path = "textedit/home.svg"
            self.clicked.connect(self.home)
        if role in ["forward", "back"]:
            self.icon_path = f"textedit/{role}.svg"
            fname_wout_ext, ext = os.path.splitext(self.icon_path)
            self.disabled_icon_path = fname_wout_ext+"_disabled"+ext
        else: self.disabled_icon_path = self.icon_path
        # hover icon path.
        fname_wout_ext, ext = os.path.splitext(self.icon_path)
        self.hover_icon_path = FigD.icon(fname_wout_ext+"_hover"+ext)
        if not os.path.exists(self.hover_icon_path):
            self.hover_icon_path = self.icon_path
        # set icon.
        self.setIcon(FigD.Icon(self.icon_path))
        # style.
        if self._is_enabled:
            self.setEnabledStyle()
        else: self.setDisabledStyle()

    def setEnabledStyle(self):
        bg_alpha = setAccentColorAlpha(self.accent_color, alpha=150)
        border_color = extractFromAccentColor(self.accent_color)
        self.setStyleSheet(jinja2.Template('''
        QToolButton {
            color: #fff;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
            border: 1px solid transparent;
        }
        QToolButton:hover {
            color: #292929;
            border: 1px solid {{ border_color }};
            background: {{ background }};
            /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''').render(
                background=bg_alpha,
                border_color=border_color,
            )
        )

    def setDisabledStyle(self):
        self.setStyleSheet('''
        QToolButton {
            color: #fff;
            font-size: 14px;
            border-radius: 2px;
            background: transparent;
            border: 1px solid transparent;
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }''')

    def enterEvent(self, event):
        if self._is_enabled:
            self.setIcon(FigD.Icon(self.hover_icon_path))
        super(FigDNavBtn, self).enterEvent(event)
        # print(f"entered {self.role}Btn")
    def leaveEvent(self, event):
        if self._is_enabled:
            self.setIcon(FigD.Icon(self.icon_path))
        super(FigDNavBtn, self).leaveEvent(event)
        # print(f"left {self.role}Btn")
    def __str__(self):
        return f"ui::__init__::FigDNavBtn(icon={self.icon_path}, role={self.role}, home_url={self.home_url}, accent_color={self.accent_color}, enabled={self._is_enabled}, max_items={self.max_items}, parent={self.parent()})"

    def setEnabled(self, enabled: bool):
        self._is_enabled = enabled
        if enabled:
            self.setEnabledStyle()
            self.setIcon(FigD.Icon(self.icon_path))
        else: 
            self.setDisabledStyle()
            self.setIcon(FigD.Icon(self.disabled_icon_path))

    def home(self):
        if self.home_url != "":
            self.browser.load(QUrl(self.home_url))

    def _reload(self):
        if self.browser: self.browser.reload()

    def back(self):
        if self.browser: self.browser.back()

    def forward(self):
        if self.browser: self.browser.forward()

    def connectBrowser(self, browser):
        self.browser = browser

    def historyItemSelected(self, index: int):
        item = self.history_items[index]
        if self.browser:
            self.browser.history().goToItem(item)

    def contextMenuEvent(self, event):
        self.contextMenu = QMenu()
        # print(f"{self.role}Btn: {event}")
        if self.role == "reload" and self.browser:
            self.contextMenu.addAction("hard reload")
            self.contextMenu.addAction("clear cache and reload")
            # print("created reload contextMenu")
        elif self.browser:
            history = self.browser.history()
            self.history_items = []
            if self.role == "back":
                for i, item in enumerate(history.backItems(self.max_items)):
                    self.contextMenu.addAction(item.title(), 
                        partial(self.historyItemSelected, i))
                    self.history_items.append(item)
            elif self.role == "forward":
                for i, item in enumerate(history.forwardItems(self.max_items)):
                    self.contextMenu.addAction(item.title(), 
                        partial(self.historyItemSelected, i))
                    self.history_items.append(item)
            self.contextMenu.addAction(FigD.Icon("textedit/history.svg"), "Show full history")
        self.contextMenu.addSeparator()
        self.contextMenu = styleContextMenu(
            self.contextMenu, 
            self.accent_color,
        )
        self.contextMenu.popup(event.globalPos())

# FigD window navigation bar.
class FigDNavBar(QWidget):
    def __init__(self, navbtns: list=[], accent_color: str="gray", 
                 search_prompt: str="Search", parent: QWidget=None) -> None:
        super(FigDNavBar, self).__init__(parent)
        self.backBtn = self.initNavBtn(role="back", accent_color=accent_color, enabled=False)
        self.forwardBtn = self.initNavBtn(role="forward", accent_color=accent_color, enabled=False)
        self.homeBtn = self.initNavBtn(role="home", accent_color=accent_color, enabled=True)
        self.reloadBtn = self.initNavBtn(role="reload", accent_color=accent_color, enabled=True)
        self.searchbar = FigDSearchBar(
            accent_color=accent_color,
            placeholder_text=search_prompt,
        )
        self.navbtns = navbtns
        # hide all buttons by default:
        self.backBtn.hide()
        self.forwardBtn.hide()
        self.homeBtn.hide()
        self.reloadBtn.hide()
        # horizontal layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(5)
        # build layout.
        self.hboxlayout.addWidget(self.backBtn)
        self.hboxlayout.addWidget(self.forwardBtn)
        self.hboxlayout.addWidget(self.reloadBtn)
        self.hboxlayout.addWidget(self.homeBtn)
        self.hboxlayout.addWidget(self.searchbar)
        # connect slot and show required buttons.
        for name in navbtns:
            getattr(self, name+"Btn").show()
        self.setLayout(self.hboxlayout)
        self.setFixedHeight(35)
        self.setGraphicsEffect(
            self.createDropShadow(accent_color)
        )

    def createDropShadow(self, accent_color: str, where: str="back"):
        drop_shadow_color = extractFromAccentColor(accent_color, where=where)
        drop_shadow = QGraphicsDropShadowEffect()
        drop_shadow.setColor(QColor(drop_shadow_color))
        drop_shadow.setBlurRadius(10)
        drop_shadow.setOffset(0, 0)

        return drop_shadow

    def navBtns(self):
        for name in self.navbtns:
            yield getattr(self, f"{name}Btn")

    def connectBrowser(self, browser) -> None:
        self.browser = browser
        for btn in self.navBtns():
            btn.connectBrowser(browser)
        self.browser.urlChanged.connect(self.refreshEnabledStatus)

    def refreshEnabledStatus(self):
        if self.browser:
            if self.browser.history().canGoBack():
                self.backBtn.setEnabled(True)
            else: self.backBtn.setEnabled(False)
            if self.browser.history().canGoForward():
                self.forwardBtn.setEnabled(True)
            else: self.forwardBtn.setEnabled(False)

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def initNavBtn(self, **args) -> QToolButton:
        btn = FigDNavBtn(**args)
        return btn

# FigD widget object.
class FigDMainWidget(QWidget):
    """
    FigDMainWidget is a regular QWidget with an API for additional tasks:
    1) ribbon menu management: toggling, simplification etc.
    2) changeZoom function for adapting to zoom changes.
    """
    # show regular ribbon menu.
    def showMenu(self):
        if hasattr(self, "menu"):
            self.menu.show()
    # hide regular ribbon menu.
    def hideMenu(self):
        if hasattr(self, "menu"):
            self.menu.hide()  
    # show simplified ribbon menu.
    def showSimplifiedMenu(self):
        if hasattr(self, "simplifiedMenu"):
            self.simplifiedMenu.show()
    # hide simplified ribbon menu.
    def hideSimplifiedMenu(self):
        if hasattr(self, "simplifiedMenu"):
            self.simplifiedMenu.hide()  
    # toggle regular ribbon menu.
    def toggleMenu(self):
        if hasattr(self, "menu"):
            if self.menu.isVisible():
                self.menu.hide()
            else: self.menu.show()
    # toggle simplified ribbon menu.
    def toggleSimplifiedMenu(self):
        if hasattr(self, "simplifiedMenu"):
            if self.simplifiedMenu.isVisible():
                self.simplifiedMenu.hide()
            else: self.simplifiedMenu.show()
    # simplify ribbon menu.
    def simplifyRibbon(self):
        self.ribbon_state = "simplified"
        self.hideMenu()
        self.showSimplifiedMenu()
    # revert to regular ribbon menu.
    def revertRibbon(self):
        self.ribbon_state = ""
        self.showMenu()
        self.hideSimplifiedMenu()
    # check if ribbon is visible.    
    def isRibbonVisible(self):
        is_visible = False
        if hasattr(self, "menu") and self.menu.isVisible():
            is_visible = True
        if hasattr(self, "simplifiedMenu") and self.simplifiedMenu.isVisible():
            is_visible = True

        return is_visible
    # show ribbon (menu or simplifiedMenu, whichever is active).
    def showRibbon(self):
        if not hasattr(self, "ribbon_state"):
            self.ribbon_state = ""
        if self.ribbon_state == "":
            self.showMenu()
            self.hideSimplifiedMenu()
        else:
            self.hideMenu()
            self.showSimplifiedMenu()
    # hide ribbon (menu or simplifiedMenu, whichever is active).
    def hideRibbon(self):
        if hasattr(self, "menu"):
            self.menu.hide()
        if hasattr(self, "simplifiedMenu"):
            self.simplifiedMenu.hide()
    # toggle current state of ribbon.
    def toggleRibbon(self):
        if self.isRibbonVisible():
            self.hideRibbon()
        else: self.showRibbon()

    def changeZoom(self, value):
        print(f"setting zoom to {value}")

# FigD main window object.
class FigDMainWindow(QMainWindow):
    """
    FigDMainWindow is a regular QMainWindow with an API for additional tasks:
    1) ribbon menu management: toggling, simplification etc.
    2) changeZoom function for adapting to zoom changes.
    """
    # show regular ribbon menu.
    def showMenu(self):
        if hasattr(self, "menu"):
            self.menu.show()
    # hide regular ribbon menu.
    def hideMenu(self):
        if hasattr(self, "menu"):
            self.menu.hide()  
    # show simplified ribbon menu.
    def showSimplifiedMenu(self):
        if hasattr(self, "simplifiedMenu"):
            self.simplifiedMenu.show()
    # hide simplified ribbon menu.
    def hideSimplifiedMenu(self):
        if hasattr(self, "simplifiedMenu"):
            self.simplifiedMenu.hide()  
    # toggle regular ribbon menu.
    def toggleMenu(self):
        if hasattr(self, "menu"):
            if self.menu.isVisible():
                self.menu.hide()
            else: self.menu.show()
    # toggle simplified ribbon menu.
    def toggleSimplifiedMenu(self):
        if hasattr(self, "simplifiedMenu"):
            if self.simplifiedMenu.isVisible():
                self.simplifiedMenu.hide()
            else: self.simplifiedMenu.show()
    # simplify ribbon menu.
    def simplifyRibbon(self):
        self.ribbon_state = "simplified"
        self.hideMenu()
        self.showSimplifiedMenu()
    # revert to regular ribbon menu.
    def revertRibbon(self):
        self.ribbon_state = ""
        self.showMenu()
        self.hideSimplifiedMenu()
    # check if ribbon is visible.    
    def isRibbonVisible(self):
        is_visible = False
        if hasattr(self, "menu") and self.menu.isVisible():
            is_visible = True
        if hasattr(self, "simplifiedMenu") and self.simplifiedMenu.isVisible():
            is_visible = True

        return is_visible
    # show ribbon (menu or simplifiedMenu, whichever is active).
    def showRibbon(self):
        if not hasattr(self, "ribbon_state"):
            self.ribbon_state = ""
        if self.ribbon_state == "":
            self.showMenu()
            self.hideSimplifiedMenu()
        else:
            self.hideMenu()
            self.showSimplifiedMenu()
    # hide ribbon (menu or simplifiedMenu, whichever is active).
    def hideRibbon(self):
        if hasattr(self, "menu"):
            self.menu.hide()
        if hasattr(self, "simplifiedMenu"):
            self.simplifiedMenu.hide()
    # toggle current state of ribbon.
    def toggleRibbon(self):
        if self.isRibbonVisible():
            self.hideRibbon()
        else: self.showRibbon()

    def changeZoom(self, value):
        print(f"setting zoom to {value}")

# shortcut description label
class FigDShortcutDescription(QLabel):
    clicked = pyqtSignal()
    def __init__(self, text: str="shortcut does...", 
                 parent: Union[None, QWidget]=None):
        super(FigDShortcutDescription, self).__init__(parent)
        self.setStyleSheet("""
        QLabel {
            color: #949494;
            font-size: 18px;
            /* font-family: 'Be Vietnam Pro'; */
            background: transparent;
        }
        QLabel:hover {
            color: #fff;
        }""")
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setText("    "+text)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super(FigDShortcutDescription, self).mousePressEvent(event)

# FigD application window object.
class FigDWindow(QMainWindow):
    def __init__(self, widget, **args):
        # set window icon, title and flags.
        super(FigDWindow, self).__init__()
        title = args.get("title", "FigD wrapped widget")
        winIcon = args.get("icon", "system/clipboard/window_icon.png")
        
        self._use_system_titlebar = False
        self._always_on_top = args.get("always_on_top", True)

        self.__win_icon_size = args.get("size", (30,30))
        self.setWindowTitle(title)
        self.setWindowIcon(FigD.Icon(winIcon))
        self.setAttribute(Qt.WA_TranslucentBackground)
        if self._always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        else: self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCentralWidget(widget)
        self.installEventFilter(self)
        self.FnF11 = FigDShortcut(
            QKeySequence("F11"), 
            self, "Toggle fullscreen mode"
        )
        self.FnF11.connect(self.toggleFullScreen)
        self.titlebar = None
        self.shortcuts_pane = self.createShortcutsPane()
        if hasattr(widget, "showMessage"):
            widget.showMessage.connect(self.statusBar().showMessage)

    def toggleUseSystemTitleBar(self):
        if self._use_system_titlebar:
            # turn off system titlebar.
            if self._always_on_top:
                self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            else:
                self.setWindowFlags(Qt.FramelessWindowHint)
        else:
            # turn on system titlebar.
            if self._always_on_top:
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
            else:
                self.setWindowFlags(Qt.WindowFlags())
        self._use_system_titlebar = not(self._use_system_titlebar)
        self.show()

    def toggleAlwaysOnTop(self):
        if self._always_on_top:
            # turn off window stays on top.
            if self._use_system_titlebar:
                self.setWindowFlags(Qt.WindowFlags())
            else:
                self.setWindowFlags(Qt.FramelessWindowHint)
        else:
            # turn on window stays on top.
            if self._use_system_titlebar:
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
            else:
                self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self._always_on_top = not(self._always_on_top)
        self.show()

    def showNormal(self):
        if self.titlebar: self.titlebar.show()
        if hasattr(self, "fullscreenBtn"):
            self.fullscreenBtn.setIcon(
                self.fullscreenBtn.fs_icon
            )
            self.fullscreenBtn.is_fullscreen = False
        super(FigDWindow, self).showNormal()

    def showFullScreen(self):
        if self.titlebar: self.titlebar.hide()
        if hasattr(self, "fullscreenBtn"):
            self.fullscreenBtn.setIcon(
                self.fullscreenBtn.efs_icon
            )
            self.fullscreenBtn.is_fullscreen = True
        super(FigDWindow, self).showFullScreen()

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else: self.showFullScreen()
        # FigD.debug("toggling fullscreen mode")
    def printShortcuts(self):
        for action in self.findChildren(QAction):
            shortcuts = [s.toString() for s in action.shortcuts()]
            if len(shortcuts) == 0: continue
            print(action.text(), shortcuts)
        # print all the shortcuts.
        for shortcut in self.findChildren(QShortcut):
            print(shortcut.key().toString()) 
            print(type(action), action.text(), action.toolTip(), [x.toString() for x in action.shortcuts()])

    def createShortcutLine(self, figd_shortcut) -> QWidget:
        shortcut = figd_shortcut.key().toString()
        action = figd_shortcut.description
        line = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        line.setLayout(layout)
        line.setStyleSheet("background: transparent;") 
        keys = shortcut.split("+")
        for key in keys[:-1]:
            keyBtn = QToolButton()
            keyBtn.setStyleSheet("""
            QToolButton {
                color: #aaa;
                padding-top: 4px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 4px;
                font-size: 16px;
                border-radius: 6px;
                background: #484848;
            }""")
            keyBtn.setText(key)
            layout.addWidget(keyBtn, 0, Qt.AlignLeft | Qt.AlignVCenter)
            # add plus as a label
            plus = QLabel()
            plus.setStyleSheet("""
            QLabel {
                color: #aaa;
                background: transparent;
            }""")
            plus.setText("+")
            layout.addWidget(plus, 0, Qt.AlignLeft | Qt.AlignVCenter)
        keyBtn = QToolButton()
        keyBtn.setStyleSheet("""
        QToolButton {
            color: #aaa;
            padding-top: 4px;
            padding-left: 8px;
            padding-right: 8px;
            padding-bottom: 4px;
            font-size: 16px;
            border-radius: 6px;
            background: #484848;
        }""")
        keyBtn.setText(keys[-1])
        layout.addWidget(keyBtn, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout.addStretch(1)
        # add description text for the action.
        description = FigDShortcutDescription(action)
        description.clicked.connect(figd_shortcut.activate)
        layout.addWidget(description)

        return line

    def createShortcutsPane(self) -> QMainWindow:
        window = QMainWindow()
        window.setAttribute(Qt.WA_TranslucentBackground)
        window.setWindowFlags(Qt.Popup)
        shortcuts_widget = QScrollArea()
        shortcuts_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        shortcuts_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        shortcuts_widget.setStyleSheet("""
        QWidget {
            border-radius: 20px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        }""")
        shortcuts_list = QWidget()
        shortcuts_list.setStyleSheet("""
        color: #eee;
        background: transparent;""")
        vboxlayout = QVBoxLayout()
        shortcuts_list.setLayout(vboxlayout)
        # account for QShortcuts.
        covered_keys = {}
        for shortcut in self.findChildren(QShortcut):
            if shortcut.key().toString() in covered_keys: continue
            if isinstance(shortcut, FigDShortcut):
                vboxlayout.addWidget(
                    self.createShortcutLine(shortcut)
                )
                covered_keys[shortcut.key().toString()] = ""
        # account for action related shortcuts not covered by QShortucts. 
        # This is populated only after QContextMenu is invoked once.
        for action in self.findChildren(QAction):
            shortcuts = [shortcut.toString() for shortcut in action.shortcuts()]
            if len(shortcuts) == 0: continue
            for shortcut in shortcuts:
                if shortcut in covered_keys: continue
                vboxlayout.addWidget(
                    self.createShortcutLine(
                        shortcut,
                        action.text(),
                    )
                )
        shortcuts_widget.setWidget(shortcuts_list)
        window.setCentralWidget(shortcuts_widget)

        return window

    def showShortcutList(self):
        self.shortcuts_pane.show()
    
    def connectTitleBar(self, titlebar):
        self.titlebar = titlebar
        self.titlebar.setWindowIcon(
            self.windowIcon(), 
            size=self.__win_icon_size,
        )
        self.titlebar.connectWindow(self)

    def define(self, *args, **kwargs):
        if self.titlebar:
            self.titlebar.define(*args, **kwargs)

def extract_colors_from_qt_grad(qt_grad: str) -> List[str]:
    return ["#"+i.split("#")[-1] for i in ("#"+"#".join(qt_grad.split(")")[0].split("#")[1:])).split(",")]

def create_css_grad(colors: List[str], angle: int=90) -> str:
    """create css gradients from a list of hex colors, and angle (in integers).

    Returns:
        str: css gradient string.
    """
    css_grad = f"linear-gradient({angle}deg, "
    css_grad += ", ".join(colors)
    css_grad += ")"

    return css_grad

FIGD_CENTRAL_WINDOW_STYLE = r"""
QMainWindow#FigDWinUI {
    border-radius: 20px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 1), stop : 0.143 rgba(22, 22, 22, 1), stop : 0.286 rgba(27, 27, 27, 1), stop : 0.429 rgba(32, 32, 32, 1), stop : 0.571 rgba(37, 37, 37, 1), stop : 0.714 rgba(41, 41, 41, 1), stop : 0.857 rgba(46, 46, 46, 1), stop : 1.0 rgba(51, 51, 51, 1));
    /* background-image: url(/home/atharva/GUI/fig-dash/resources/icons/textedit/NoiseGaussBlur(5).png); */
}
QScrollBar:vertical {
    border: 0px solid #999999;
    width: 12px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0);
}
QScrollBar:horizontal {
    border: 0px solid #999999;
    width: 12px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0);
}
/* QScrollBar:vertical:hover {
    background-color: rgba(255, 253, 184, 0.3);
} */
QScrollBar::handle:vertical {
    min-height: 0px;
    border: 0px solid red;
    border-radius: 0px;
    /* background-color: transparent; */
    background-color: rgba(255, 255, 255, 0.2);
}
QScrollBar::handle:horizontal {
    min-width: 0px;
    border: 0px solid red;
    border-radius: 0px;
    /* background-color: transparent; */
    background-color: rgba(255, 255, 255, 0.2);
}
QScrollBar::handle:vertical:hover {
    background-color: rgba(255, 255, 255, 0.5);
}
QScrollBar::handle:horizontal:hover {
    background-color: rgba(255, 255, 255, 0.5);
}
QScrollBar::add-line:horizontal {
    width: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    width: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical {
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}"""
FIGD_CENTRAL_WIDGET_STYLE = r"""
QWidget#FigDUI {
    border-radius: 20px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 1), stop : 0.143 rgba(22, 22, 22, 1), stop : 0.286 rgba(27, 27, 27, 1), stop : 0.429 rgba(32, 32, 32, 1), stop : 0.571 rgba(37, 37, 37, 1), stop : 0.714 rgba(41, 41, 41, 1), stop : 0.857 rgba(46, 46, 46, 1), stop : 1.0 rgba(51, 51, 51, 1));
}
QScrollBar:vertical {
    border: 0px solid #999999;
    width: 12px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0);
}
QScrollBar:horizontal {
    border: 0px solid #999999;
    width: 12px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0);
}
/* QScrollBar:vertical:hover {
    background-color: rgba(255, 253, 184, 0.3);
} */
QScrollBar::handle:vertical {
    min-height: 0px;
    border: 0px solid red;
    border-radius: 0px;
    /* background-color: transparent; */
    background-color: rgba(255, 255, 255, 0.2);
}
QScrollBar::handle:horizontal {
    min-width: 0px;
    border: 0px solid red;
    border-radius: 0px;
    /* background-color: transparent; */
    background-color: rgba(255, 255, 255, 0.2);
}
QScrollBar::handle:vertical:hover {
    background-color: rgba(255, 255, 255, 0.5);
}
QScrollBar::handle:horizontal:hover {
    background-color: rgba(255, 255, 255, 0.5);
}
QScrollBar::add-line:horizontal {
    width: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    width: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical {
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}"""
def wrapFigDWindow(widget: QWidget, **args):
    # arguments.
    icon = args.get("icon")
    title = args.get("title", "")
    width = args.get("width", 960)
    height = args.get("height", 800)
    _where = args.get("where", "front")
    font_color = args.get("font_color")
    add_tabs = args.get("add_tabs", True)
    autohide = args.get("autohide", True)
    animated = args.get("animated", False)
    app_name = args.get("app_name", "Unknown")
    show_titlebar = args.get("titlebar", True)
    accent_color = args.get("accent_color", "white")
    find_function = args.get("find_function")
    bookmark_manager = args.get("bookmark_manager")
    titlebar_callbacks = args.get("titlebar_callbacks", {})
    # create the titlebar.
    from fig_dash.ui.titlebar import WindowTitleBar
    titlebar = WindowTitleBar(
        background=accent_color, callbacks=titlebar_callbacks,
        title_widget=args.get("title_widget"), where=_where, 
        ctrl_btns_loc=args.get("ctrl_btns_loc", "right"),
    )
    settingsMenu = FigDAppSettingsMenu(
        tabs_enabled=add_tabs,
        accent_color=accent_color,
    )
    titlebar.settingsBtn.setContextMenu(settingsMenu)
    settingsMenu = styleContextMenu(settingsMenu, accent_color, 
                                    padding=5, font_size=18)
    settingsMenu.notifsMenu = styleContextMenu(
        settingsMenu.notifsMenu, accent_color,
        padding=5, font_size=18,
    )
    for slider in settingsMenu.sliders:
        slider.setAccentColor(accent_color)
    tab_icon = args.get("tab_icon", "icon.svg")
    tab_title = args.get("tab_title", "New tab")
    if animated: titlebar.setAnimatedTitle(title)
    else: titlebar.setTitle(title)
    # connect functionalities of ribbon collapse button and associated menu with widget's ribbon management API
    rcb = titlebar.ribbonCollapseBtn
    for api_func, slot in {
            "toggleRibbon": rcb.clicked, 
            "showRibbon": rcb.showRibbon.triggered, 
            "hideRibbon": rcb.hideRibbon.triggered,
            "simplifyRibbon": rcb.simplifyRibbon.triggered,
        }.items():
        if hasattr(widget, api_func): 
            slot.connect(getattr(widget, api_func))
        else: pass # print(f"widget/window of type `{type(widget)}` doesnt't have `{api_func}` in its API")
    # if show_titlebar is false then hide titlebar.
    if not show_titlebar: titlebar.hide()
    centralWindow = QMainWindow()
    centralWindow.setObjectName("FigDWinUI")
    centralWindow.setStyleSheet(FIGD_CENTRAL_WINDOW_STYLE)
    # centralWindow.statusBar().showMessage("STATUS BAR")
    centralWidget = QWidget()
    centralWidget.setObjectName("FigDUI")
    centralWidget.setStyleSheet(FIGD_CENTRAL_WIDGET_STYLE)
    
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(8, 2, 8, 0)

    centralWindow.addToolBar(Qt.TopToolBarArea, titlebar)
    # build layout.
    # layout.addWidget(titlebar)
    if add_tabs:
        tabwidget = FigDTabWidget(
            tab_title=tab_title, tab_icon=tab_icon,
            widget_args=args.get("widget_args", {}),
            window_args=args.get("window_args", {}),
            widget_factory=args.get("widget_factory"),
            window_factory=args.get("window_factory"),
            accent_color=accent_color, where=_where,
            autohide=autohide,
        )
        tabwidget.connectTitleBar(titlebar)
        tabwidget.changeWindowTitle.connect(titlebar.setTitle)
        titlebar.showTabBar.connect(tabwidget.tabBar().show)
        titlebar.hideTabBar.connect(tabwidget.tabBar().hide)
        # connects slots to optionally defined widget signals.
        widget = tabwidget.wrapWidget(widget, titlebar)
        tabwidget.tabFactory(widget)
        # tabwidget.addTab(widget, QIcon(tab_icon), tab_title)
        layout.addWidget(tabwidget)
        tabwidget.CtrlShiftW = FigDShortcut(
            QKeySequence("Ctrl+Shift+W"),
            tabwidget, "Close app window",
        )
    else:
        widget.CtrlW = FigDShortcut(QKeySequence.Close, 
                                    widget, "Close app window")
        layout.addWidget(widget)
    try:
        layout.addWidget(widget.statusbar)
    except Exception as e: print(e)
    centralWidget.setLayout(layout)
    centralWindow.setCentralWidget(centralWidget)
    window = FigDWindow(widget=centralWindow, **args)
    window.appName = app_name
    window.find_function = find_function
    window.bookmark_manager = bookmark_manager
    if not add_tabs: 
        widget.CtrlW.connect(window.close)
    else:
        window.tabs = tabwidget
        tabwidget.CtrlShiftW.connect(window.close)
    window.setWindowOpacity(1)
    window.connectTitleBar(titlebar)
    window.AltShiftR = FigDShortcut(QKeySequence("Alt+Shift+R"), 
                                    window, "Rename current window")
    window.AltShiftR.connect(titlebar.triggerRenameWindow)
    settingsMenu.connectWindow(window)
    if add_tabs: window.tabs = tabwidget
    window = prepStatusBar(
        window, accent_color=accent_color, 
        font_color=font_color, where=_where,
    )
    zoomSlider = window.zoomControls
    # react to change in zoom acc. to the slider/label.
    if add_tabs:
        zoomSlider.zoomChanged.connect(tabwidget.changeZoom)
    elif hasattr(widget, "changeZoom"):
        zoomSlider.zoomChanged.connect(widget.changeZoom)
    if add_tabs:
        tabwidget.zoomChanged.connect(
            zoomSlider.setValueOnTabChange
        )
    # menu many not exist.

    if hasattr(widget, "toggleRibbon"):
        window.CtrlShiftM = FigDShortcut(
            QKeySequence("Ctrl+Shift+M"), window,
            "Toggle ribbon menu"
        )
        if add_tabs:
            window.CtrlShiftM.connect(
                partial(tabwidget.onCurrentWidget, "toggleRibbon")
            )
        else: window.CtrlShiftM.connect(widget.toggleRibbon)
    # connect full screen action.
    try:
        fa = titlebar.maximizeBtn.fullscreen # full screen action.
        fa.triggered.connect(window.showFullScreen) # show full screen om trigger.
    except Exception as e: print(e)
    # connect exit full screen action.
    try:
        efa = titlebar.maximizeBtn.exit_fullscreen # exit full screen action.
        efa.triggered.connect(window.showNormal) # show normal on trigger.
    except Exception as e: print(e)
    # style application tooltips
    app = QApplication.instance()
    if icon: app.createTrayIcon(tray_icon=icon)
    app.setStyleSheet("""
    QToolTip {
        color: #fff;
        border: 0px;
        padding-top: -1px;
        padding-left: 5px;
        padding-right: 5px;
        padding-bottom: -1px;
        font-size:  17px;
        background: #000;
        font-family: 'Be Vietnam Pro', sans-serif;
    }""")
    # try: app.appendTitleBar(titlebar)
    # except Exception as e: print(e)
    # reposition window
    window.setGeometry(100, 100, width, height)
    screen_rect = app.desktop().screenGeometry()
    x = (screen_rect.width()-width) // 2
    y = (screen_rect.height()-height) // 2
    widget.window_ptr = window
    window.move(x, y)

    return window
# def styleWindowStatusBar(window: QMainWindow, widget: Union[QWidget, None]=None, 
#                          accent_color: Union[str, None]=None, where: str="back",
#                          apply_style_sheet: bool=True, font_color: str="#fff") -> QMainWindow:
#     """Shifts a windows statusbar from the transparent QMainWindow to the window object.
#     Args:
#         window (QMainWindow): A QMainWindow or FigDWindow object.
#         windget (QWidget, optional): The widget wrapped around in the FigDWindow. Defaults to None.
#         accent_color (str, optional): Accent color of the window.
#         apply_style_sheet (bool, optional): Whether statusBar style sheet should be updated. Defaults to True.
#         widget
#         font_color (str, optional): Color of the statusbar font. Defaults to "#fff".
#     Returns:
#         QMainWindow: returns rearranged FigDWindow/QMainWindow object.
#     """
#     assert isinstance(window, QMainWindow), f"window object is of type `{type(window)}`. Expecting QMainWindow type object instead."
#     statusBar = window.statusBar()
#     window.statusbar = statusBar
#     window.centralWidget().layout().addWidget(window.statusbar, 0, Qt.AlignCenter)
#     # if the wrapped widget has a "statusbar" attribute then add it to statusbar.
#     if widget is not None and hasattr(widget, "statusbar"):
#         window.statusbar.addWidget(widget.statusbar)
#     if apply_style_sheet:
#         if accent_color:
#             fontColor = extractFromAccentColor(accent_color, where=where)
#         else: fontColor = font_color
#         window.statusbar.setStyleSheet("""
#         QStatusBar {
#             color: """+fontColor+""";
#             font-size: 17px;
#             font-family: "Be Vietnam Pro";
#             background: transparent;
#         }""")

#     return window
# prepare status bar: style it, add zoom controls etc.
def prepStatusBar(window: QMainWindow, accent_color: Union[str, None]=None, 
                  where: str="back", apply_style_sheet: bool=True, 
                  font_color: Union[str, None]=None) -> QMainWindow:
    """style the centralWindow.
    Args:
        window (QMainWindow): A QMainWindow or FigDWindow object.
        accent_color (str, optional): Accent color of the window.
        apply_style_sheet (bool, optional): Whether statusBar style sheet should be updated. Defaults to True.
        widget
        font_color (str, optional): Color of the statusbar font. Defaults to "#fff".
    Returns:
        QMainWindow: returns rearranged FigDWindow/QMainWindow object.
    """
    WindowErrorMsg = f"""window object is of type `{type(window)}`. 
Expecting QMainWindow type object instead."""
    CentralWidgetErrorMsg = f"""centralWidget object is of type `{type(window.centralWidget())}`. 
Expecting QMainWindow type object instead."""
    assert isinstance(window, QMainWindow), WindowErrorMsg
    assert isinstance(window.centralWidget(), QMainWindow), CentralWidgetErrorMsg
    statusBar = window.centralWidget().statusBar()
    statusBar.setSizeGripEnabled(False)
    if apply_style_sheet:
        if font_color is None:
            font_color = extractFromAccentColor(
                bg=accent_color, 
                where=where,
            )
        statusBar.setStyleSheet("""
        QStatusBar {
            color: """+font_color+""";
            font-size: 17px;
            font-family: "Be Vietnam Pro";
            background: transparent;
        }""")
    from fig_dash.ui.titlebar import FullScreenBtn
    fullscreenBtn = FullScreenBtn(
        fs_icon="titlebar/fullscreen.svg", 
        efs_icon="titlebar/exit_fullscreen.svg", 
        style="r", background=accent_color,
    )
    window.fullscreenBtn = fullscreenBtn
    zoomControls = FigDZoomSlider(
        text=" ", value=135, plus=True, minus=True, 
        minm=25, maxm=250, btns_list=[fullscreenBtn],
        set_status_tip=False, accent_color=accent_color,
    )
    # zoomControls.hboxlayout.setSpacing(0)
    zoomControls.label.setStyleSheet("""
    QLabel {
        color: #fff;
        font-size: 16px;
        background: transparent;
        font-family: "Be Vietnam Pro";
    }""")
    # zoomControls.plusBtn.setIcon(FigD.Icon("widget/zoom_in.png"))
    # zoomControls.minusBtn.setIcon(FigD.Icon("widget/zoom_out.png"))
    zoomControls.readout.setFixedWidth(40)
    zoomControls.connectWindow(window)
    zoomControls.setFixedHeight(35)
    window.zoomControls = zoomControls
    statusBar.addPermanentWidget(zoomControls)

    return window