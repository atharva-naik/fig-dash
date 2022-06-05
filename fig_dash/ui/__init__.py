#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::__init__")
import os
import jinja2
from typing import *
from pathlib import Path
from functools import partial
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.titlebar import TitleBar, WindowTitleBar, ZoomSlider
# PyQt5 imports
# from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtGui import QFontDatabase, QColor, QPalette, QIcon, QKeySequence
from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMenu, QFrame, QAction, QWidget, QMainWindow, QTabWidget, QLabel, QToolButton, QVBoxLayout, QHBoxLayout, QGridLayout, QSystemTrayIcon, QScrollArea, QShortcut, QSlider, QLineEdit


class FigDShortcut(QShortcut):
    def __init__(self, keyseq: QKeySequence, 
                 parent: Union[None, QWidget]=None,
                 description: str="description"):
        super(FigDShortcut, self).__init__(keyseq, parent)
        self.description = description


class DashWidgetGroupBtnStyler:
    def __init__(self):
        self.templates = {}

    def __call__(self, style, **options):
        return self.templates[style]

class DashWidgetGroupStyler:
    pass

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
    "&Undo	Ctrl+Z": (
        FigD.icon("textedit/undo.svg"),
        FigD.icon("textedit/undo_disabled.svg")
    ),
    "&Redo	Ctrl+Shift+Z": (
        FigD.icon("textedit/redo.svg"),
        FigD.icon("textedit/redo_disabled.svg")
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

def styleTextEditMenuIcons(menu):
    """substitute TextEdit/LineEdit icons for consistent styling."""
    for action in menu.actions():
        # print(action.text())
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

def styleContextMenu(menu, accent_color: str="yellow", 
                     padding: int=5, font_size: int=18):
    menu.setAttribute(Qt.WA_TranslucentBackground)
    menu.setObjectName("FigDMenu")
    menu.setStyleSheet(jinja2.Template("""
    QMenu#FigDMenu {
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
    	color: #fff;
    	padding: 10px;
    	border-radius: 15px;
        font-size: {{ FONT_SIZE }}px;
        font-family: "Be Vietnam Pro";
    }
    QMenu#FigDMenu::item {
        padding: {{ PADDING }}px;
    }
    QMenu#FigDMenu::item:selected {
    	color: #292929; 
        border-radius: 5px;
    	background-color: {{ ACCENT_COLOR }}; 
    }
    QMenu#FigDMenu:separator {
    	background: #292929;
    }""").render(
        ACCENT_COLOR=accent_color, 
        FONT_SIZE=font_size, PADDING=padding
    ))
    palette = menu.palette()
    palette.setColor(QPalette.Base, QColor(48,48,48))
    palette.setColor(QPalette.Text, QColor(125,125,125))
    palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    # palette.setColor(QPalette.PlaceholderText, QColor(125,125,125))
    palette.setColor(QPalette.Window, QColor(255,255,255))
    palette.setColor(QPalette.Highlight, QColor(235,95,52))
    menu.setPalette(palette)

    return menu

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
        # stylesheet attributes.
        background = args.get("background", "transparent")
        # print(font_size)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        elif self.hover_response == "background":
            self.setStyleSheet(jinja2.Template('''
            QToolButton {
                color: #fff;
                border: 0px;
                font-size: 14px;
                border-radius: 5px;
                background: transparent;
            }
            QToolButton:hover {
                color: #292929;
                background: {{ background }};
                /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
            }
            QToolTip {
                color: #fff;
                border: 0px;
                background: #000;
            }''').render(
                    background=background,
                )
            )
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
            print(f"{self.groupLabelName.text()}: layout.setSpacing({spacing})")
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
        # print("\x1b[34;1menterEvent\x1b[0m")
        self.setBackgroundColor((255,255,255,50))
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

# dash widget ribbon menu.
class DashRibbonMenu(QWidget):
    def __init__(self, group_names: List[str]=[], 
                 parent: Union[None, QWidget]=None,
                 contents_margins=(5, 0, 5, 0),
                 accent_color: str="gray"):
        super(DashRibbonMenu, self).__init__(parent)
        self.accent_color = accent_color
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
                parent=parent, name=name, 
                accent_color=accent_color
            )
            self.hboxlayout.addWidget(self.__group_widget_map[name])
            self.hboxlayout.addWidget(self.addSeparator())
        name = self.__group_names[-1]
        self.__group_widget_map[name] = DashWidgetGroup(
            parent=parent, name=name,
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
        self.active_window_ptr = None
        # tray_icon = args.get("icon", "lol")
        # create tray menu.
        self.trayMenu = self.initTrayMenu()

    def createTrayIcon(self, tray_icon: str):
        # tray icon button.
        self.trayIcon = QSystemTrayIcon(FigD.Icon(tray_icon), self)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

    def initTrayMenu(self) -> QMenu:
        """create context menu for system tray icon.

        Returns:
            QMenu: context menu object.
        """
        # actions for tray icon context menu.
        self.showAction = QAction("Open")
        self.quitAction = QAction("Quit")
        # self.logsAction = QAction("Get logs")
        # self.supportAction = QAction("Collect support files")
        self.settingsAction = QAction("Settings")
        # add icons.
        self.showAction.setIcon(FigD.Icon("tray/open.svg"))
        self.quitAction.setIcon(FigD.Icon("tray/close.svg"))
        # self.logsAction.setIcon(FigD.Icon("tray/logs.svg"))
        # self.supportAction.setIcon(FigD.Icon("tray/logs.svg"))
        self.settingsAction.setIcon(FigD.Icon("tray/settings.svg"))
        # connect functions to actions.
        self.showAction.triggered.connect(self.showActiveWindow)
        self.quitAction.triggered.connect(self.quit)
        # tray icon menu.
        trayMenu = QMenu()
        # trayMenu.addAction(self.logsAction)
        # trayMenu.addAction(self.supportAction)
        # trayMenu.addSeparator()
        trayMenu.addAction(self.settingsAction)
        trayMenu.addSeparator()
        trayMenu.addAction(self.showAction)
        trayMenu.addAction(self.quitAction)

        return trayMenu

    def showActiveWindow(self):
        window = QApplication.activeWindow()
        window.show()

    def notify(self, obj, event):
        if isinstance(obj, FigDWindow):
            if event.type() == QEvent.WindowDeactivate:
                # print("deactivated", obj.appName)
                obj.titlebar.deactivate()
            if event.type() == QEvent.WindowActivate:
                # print("activated", obj.appName)
                obj.titlebar.activate()

        return super(FigDAppContainer, self).notify(obj, event)


class FigDTabWidget(QTabWidget):
    def __init__(self, widget_factory=None, window_factory=None, 
                parent: Union[None, QWidget]=None, 
                widget_args={}, window_args={}):
        super(FigDTabWidget, self).__init__(parent)
        self.window_factory = window_factory
        self.widget_factory = widget_factory
        self.window_args = window_args
        self.widget_args = widget_args 
        self.setStyleSheet("""
        QTabWidget {
            color: #fff;
            border: 0px;
            font-family: 'Be Vietnam Pro';
            background: transparent;
        }
        QTabWidget::pane {
            border: 0px;
            background: transparent;
        }
        QTabBar {
            border: 0px;
            background: transparent;
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
            border: 0px;
            color: #fff;

            margin-left: 1px;
            margin-right: 1px;

            padding-top: 5px;
            padding-left: 9px;
            padding-right: 5px;
            padding-bottom: 5px;

            font-size: 17px;
            font-family: 'Be Vietnam Pro', sans-serif;
            max-width: 300px;
            background: #000;
        }
        QTabBar::tab:hover {
            color: #fff;
            background: #323232;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 200), stop : 0.3 rgba(191, 54, 54, 220), stop : 0.6 rgba(235, 95, 52, 220), stop: 0.9 rgba(235, 204, 52, 220)); */
        }
        QTabBar::tab:selected {
            color: #eee;
            border: 0px;
            background: #323232;
            font-weight: bold;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #e4852c, stop : 0.143 #e4822d, stop : 0.286 #e4802f, stop : 0.429 #e47d30, stop : 0.571 #e47b32, stop : 0.714 #e47833, stop : 0.857 #e47635, stop : 1.0 #e47336); */
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 rgba(161, 31, 83, 220), stop : 0.3 rgba(191, 54, 54, 220), stop: 0.9 rgba(235, 95, 52, 220)); */
            padding-top: 5px;
            padding-left: 9px;
            padding-right: 5px;
            padding-bottom: 5px;
            margin-left: 1px;
            margin-right: 1px;
            font-size: 17px;
            font-weight: bold;
        }""")
        # set stuff.
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setDocumentMode(False)
        self.setTabBarAutoHide(True)
        self.setElideMode(Qt.ElideRight)
        self.setObjectName("FigDTabWidget")
        # connect slots to signals.
        self.currentChanged.connect(self.onTabChange)
        self.tabCloseRequested.connect(self.removeTab)
        # shortcuts
        self.AddTab = FigDShortcut(QKeySequence.AddTab, self, "Open new tab")
        self.AddTab.activated.connect(self.openTab)
        self.NewWindow = FigDShortcut(QKeySequence.New, self, "Open new window")
        self.NewWindow.activated.connect(self.openWindow)
        self.CloseTab = FigDShortcut(QKeySequence.Close, self, "Close tab/window")
        self.CloseTab.activated.connect(self.closeCurrentTab)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def onTabChange(self):
        widget = self.currentWidget()
        # if hasattr(widget, "signalZoom"):
        #     widget.signalZoom()
    def connectTitleBar(self, titlebar):
        self.titlebar = titlebar

    def closeCurrentTab(self):
        i = self.currentIndex()
        if i == 0: 
            QApplication.activeWindow().close()
        else: self.removeTab(i)

    def changeCurrentTabTitle(self, title: str):
        i = self.currentIndex()
        print(title)
        self.setTabText(i, title)

    def changeCurrentTabIcon(self, icon: str):
        i = self.currentIndex()
        self.setTabIcon(i, QIcon(icon))

    def openTab(self):
        # print(f"self.widget_factory: {self.widget_factory}")
        if self.widget_factory is None: return
        widget = self.widget_factory(**self.widget_args)
        if hasattr(widget, "changeTabTitle"):
            widget.changeTabTitle.connect(self.changeCurrentTabTitle)
        if hasattr(widget, "changeTabIcon"):
            widget.changeTabTitle.connect(self.changeCurrentTabIcon)
        if hasattr(widget, "zoomChanged") and hasattr(self, "titlebar"):
            widget.zoomChanged.connect(self.titlebar.zoomSlider.setZoomValue)
        self.addTab(widget, FigD.Icon("system/fileviewer/new_tab_icon.svg"), "Home")
        self.setCurrentIndex(self.count())

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

# FigD window object.
class FigDWindow(QMainWindow):
    def __init__(self, widget, **args):
        # self.layout.insertWidget(0, titlebar)
        # set window icon, title and flags.
        super(FigDWindow, self).__init__()
        title = args.get("title", "FigD wrapped widget")
        winIcon = args.get("icon", "system/clipboard/window_icon.png")
        self.__win_icon_size = args.get("size", (30,30))
        self.setWindowTitle(title)
        self.setWindowIcon(FigD.Icon(winIcon))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setCentralWidget(widget)
        self.installEventFilter(self)
        self.titlebar = None
        self.shortcuts_pane = self.createShortcutsPane()

    def printShortcuts(self):
        for action in self.findChildren(QAction):
            shortcuts = [s.toString() for s in action.shortcuts()]
            if len(shortcuts) == 0: continue
            print(action.text(), shortcuts)
        # print all the shortcuts.
        for shortcut in self.findChildren(QShortcut):
            print(shortcut.key().toString()) 
            # print(type(action), action.text(), action.toolTip(), [x.toString() for x in action.shortcuts()])
    def createShortcutLine(self, shortcut: str, action: str) -> QWidget:
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
        description = QLabel()
        description.setStyleSheet("""
        QLabel {
            color: #fff;
            font-size: 16px;
            font-family: 'Be Vietnam Pro';
            background: transparent;
        }""")
        description.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        description.setText(action)
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
            if isinstance(shortcut, FigDShortcut):
                vboxlayout.addWidget(
                    self.createShortcutLine(
                        shortcut.key().toString(),
                        shortcut.description,
                    )
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
        # self.printShortcuts()
        return window
    # def focusInEvent(self, event):
    #     if self.titlebar: self.titlebar.activate()
    #     super(FigDWindow, self).focusInEvent(event)
    # def focusOutEvent(self, event):
    #     if self.titlebar: self.titlebar.deactivate()
    #     super(FigDWindow, self).focusOutEvent(event)
        # self.setStyleSheet("""
        # QMainWindow {
        #     border-radius: 20px;
        #     background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        # }""")
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

def wrapFigDWindow(widget: QWidget, **args):
    QFontDatabase.addApplicationFont(
        FigD.font("BeVietnamPro-Regular.ttf")
    )
    # arguments.
    icon = args.get("icon")
    title = args.get("title", "")
    width = args.get("width", 960)
    height = args.get("height", 800)
    _where = args.get("where", "front")
    add_tabs = args.get("add_tabs", True)
    animated = args.get("animated", False)
    show_titlebar = args.get("titlebar", True)
    accent_color = args.get("accent_color", "red")
    titlebar_callbacks = args.get("titlebar_callbacks", {})
    # create the titlebar.
    titlebar = WindowTitleBar(
        background=accent_color, 
        callbacks=titlebar_callbacks,
        title_widget=args.get("title_widget"),
        where=_where,
    )
    tab_icon = args.get("tab_icon", "icon.svg")
    tab_title = args.get("tab_title", "New tab")
    if animated: titlebar.setAnimatedTitle(title)
    else: titlebar.setTitle(title)
    # menu many not exist.
    try:
        titlebar.ribbonCollapseBtn.clicked.connect(widget.menu.toggle)
        # menu hide action.
        hide_action = titlebar.ribbonCollapseBtn.hidemenu
        # connect hide action to menu.hide
        hide_action.triggered.connect(widget.menu.hide)
    except Exception as e: print(e)
    # simplifyMenu function may not exist.
    try:
        # simplification action.
        simplify_action = titlebar.ribbonCollapseBtn.simplify
        # connect simplify action to the simplified menu toggle if it exists.
        simplify_action.triggered.connect(widget.simplifyMenu)
    except Exception as e: print(e)
    # if show_titlebar is false then hide titlebar.
    if not show_titlebar: titlebar.hide()
    centralWidget = QWidget()
    centralWidget.setObjectName("FigDUI")
    centralWidget.setStyleSheet("""
    QWidget#FigDUI {
        border-radius: 20px;
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
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
    }""")
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    # build layout.
    layout.addWidget(titlebar)
    if add_tabs:
        tabwidget = FigDTabWidget(
            widget_args=args.get("widget_args", {}),
            window_args=args.get("window_args", {}),
            widget_factory=args.get("widget_factory"),
            window_factory=args.get("window_factory"),
        )
        tabwidget.connectTitleBar(titlebar)
        # print(f"tab_icon: {tab_icon}")
        if hasattr(widget, "changeTabTitle"):
            widget.changeTabTitle.connect(tabwidget.changeCurrentTabTitle)
        if hasattr(widget, "changeTabIcon"):
            widget.changeTabTitle.connect(tabwidget.changeCurrentTabIcon)
        if hasattr(widget, "zoomChanged") and hasattr(tabwidget, "titlebar"):
            widget.zoomChanged.connect(titlebar.zoomSlider.setZoomValue)
        tabwidget.addTab(widget, QIcon(tab_icon), tab_title)
        layout.addWidget(tabwidget)
    else:
        layout.addWidget(widget)
    try:
        layout.addWidget(widget.statusbar)
    except Exception as e: print(e)
    centralWidget.setLayout(layout)

    window = FigDWindow(widget=centralWidget, **args)
    window.appName = title
    window.connectTitleBar(titlebar)
    # changeZoom function may not exist.
    try:
        zoomSlider = titlebar.zoomSlider
        # react to change in zoom acc. to the slider/label.
        if add_tabs:
            zoomSlider.zoomChanged.connect(tabwidget.changeZoom)
        else:
            zoomSlider.zoomChanged.connect(widget.changeZoom)
    except Exception as e: print(e)
    # menu many not exist.
    try:
        window.CtrlShiftM = FigDShortcut(
            QKeySequence("Ctrl+Shift+M"), window,
            "Toggle ribbon menu"
        )
        window.CtrlShiftM.activated.connect(widget.menu.toggle)
    except Exception as e: print(e)
    # connect full screen action.
    try:
        # full screen action.
        fullscreen_action = titlebar.maximizeBtn.fullscreen
        # connect full screen action to show full screen
        fullscreen_action.triggered.connect(window.showFullScreen)
    except Exception as e: print(e)
    # connect exit full screen action.
    try:
        # exit full screen action.
        exit_fullscreen_action = titlebar.maximizeBtn.exit_fullscreen
        # connect exit full screen action to show normal.
        exit_fullscreen_action.triggered.connect(window.showNormal)
    except Exception as e: print(e)
    # style application tooltips
    app = QApplication.instance()
    if icon is not None:
        app.createTrayIcon(tray_icon=icon)
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
    w, h = screen_rect.width()//2, screen_rect.height()//2
    widget.window_ptr = window
    window.move(w, h)

    return window

def styleWindowStatusBar(window: QMainWindow, widget: Union[QWidget, None]=None, 
                         accent_color: Union[str, None]=None, where: str="back",
                         apply_style_sheet: bool=True, font_color: str="#fff") -> QMainWindow:
    """Shifts a windows statusbar from the transparent QMainWindow to the window object.
    Args:
        window (QMainWindow): A QMainWindow or FigDWindow object.
        windget (QWidget, optional): The widget wrapped around in the FigDWindow. Defaults to None.
        accent_color (str, optional): Accent color of the window.
        apply_style_sheet (bool, optional): Whether statusBar style sheet should be updated. Defaults to True.
        widget
        font_color (str, optional): Color of the statusbar font. Defaults to "#fff".
    Returns:
        QMainWindow: returns rearranged FigDWindow/QMainWindow object.
    """
    assert isinstance(window, QMainWindow), f"window object is of type `{type(window)}`. Expecting QMainWindow type object instead."
    statusBar = window.statusBar()
    window.statusbar = statusBar
    window.centralWidget().layout().addWidget(window.statusbar)
    # if the wrapped widget has a "statusbar" attribute then add it to statusbar.
    if widget is not None and hasattr(widget, "statusbar"):
        window.statusbar.addWidget(widget.statusbar)
    if apply_style_sheet:
        if accent_color:
            fontColor = extractFromAccentColor(accent_color, where=where)
        else: fontColor = font_color
        window.statusbar.setStyleSheet("""
        QStatusBar {
            color: """+fontColor+""";
            font-size: 17px;
            font-family: "Be Vietnam Pro";
            background: transparent;
        }""")

    return window