#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Gradient Creator for Qt, CSS and SVG
import os
import re
import sys
import jinja2
from typing import *
from functools import partial
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.browser import DebugWebView
from fig_dash.ui.js.webchannel import QWebChannelJS
from fig_dash.ui.apps import AppIconMap, AppTitleMap, AccentColorMap, TitleBarAccentColorMap
from fig_dash.ui import wrapFigDWindow, styleContextMenu, styleWindowStatusBar, FigDAppContainer, FigDShortcut, DashSlider
# PyQt5 imports
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSlot, pyqtSignal, QObject, QThread, QFileSystemWatcher
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QToolBar, QMenu, QToolButton, QSizePolicy, QAction, QActionGroup, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QComboBox, QScrollArea

# gradient radio button styles.
GRADIENT_RADIO_BTN_STYLE_L = jinja2.Template("""
QToolButton {
    color: #fff;
    padding: 10px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.091 #2e2e2e, stop : 0.182 #333333, stop : 0.273 #383838, stop : 0.364 #3d3d3d, stop : 0.455 #424242, stop : 0.545 #474747, stop : 0.636 #4c4c4c, stop : 0.727 #525252, stop : 0.818 #575757, stop : 0.909 #5d5d5d, stop : 1.0 #626262);
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}
QToolButton:hover {
    color: #292929;
    background: {{ ACCENT_COLOR }}; 
}""")
GRADIENT_RADIO_SEL_BTN_STYLE_L = jinja2.Template("""
QToolButton {
    padding: 10px;
    color: #292929;
    font-weight: bold;
    background: {{ ACCENT_COLOR }}; 
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}""")
GRADIENT_RADIO_BTN_STYLE_C = jinja2.Template("""
QToolButton {
    color: #fff;
    padding: 10px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.091 #2e2e2e, stop : 0.182 #333333, stop : 0.273 #383838, stop : 0.364 #3d3d3d, stop : 0.455 #424242, stop : 0.545 #474747, stop : 0.636 #4c4c4c, stop : 0.727 #525252, stop : 0.818 #575757, stop : 0.909 #5d5d5d, stop : 1.0 #626262);
}
QToolButton:hover {
    color: #292929;
    background: {{ ACCENT_COLOR }}; 
}""")
GRADIENT_RADIO_SEL_BTN_STYLE_C = jinja2.Template("""
QToolButton {
    color: #292929;
    padding: 10px;
    font-weight: bold;
    background: {{ ACCENT_COLOR }}; 
}""")
GRADIENT_RADIO_BTN_STYLE_R = jinja2.Template("""
QToolButton {
    color: #fff;
    padding: 10px;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.091 #2e2e2e, stop : 0.182 #333333, stop : 0.273 #383838, stop : 0.364 #3d3d3d, stop : 0.455 #424242, stop : 0.545 #474747, stop : 0.636 #4c4c4c, stop : 0.727 #525252, stop : 0.818 #575757, stop : 0.909 #5d5d5d, stop : 1.0 #626262);
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}
QToolButton:hover {
    color: #292929;
    background: {{ ACCENT_COLOR }}; 
}""")
GRADIENT_RADIO_SEL_BTN_STYLE_R = jinja2.Template("""
QToolButton {
    padding: 10px;
    color: #292929;
    font-weight: bold;
    background: {{ ACCENT_COLOR }}; 
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}""")

# validate hex color string.
def validate_hex_color(hexstr: str) -> bool:
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexstr) is None: return False
    return True

# Radio button made from QToolButtons.
class GradientRadioButton(QWidget):
    indexChanged = pyqtSignal(int)
    optionChanged = pyqtSignal(str)
    def __init__(self, options: List[str], accent_color: str, 
                 title: str="", parent: Union[None, QWidget]=None):
        super(GradientRadioButton, self).__init__(parent)
        self.options = options
        self.accent_color = accent_color
        # main layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        # horizontal layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        # horizontal box.
        self.hbox = QWidget()
        self.hbox.setStyleSheet("background: transparent; border: 0px")
        self.hbox.setLayout(self.hboxlayout)
        
        self.i = 0 # selected button index.
        self.btns = [] # list of buttons.

        self.hboxlayout.addStretch(1)
        # left button.
        lbtn = self.initBtn(options[0], role="l")
        lbtn.setStyleSheet(GRADIENT_RADIO_SEL_BTN_STYLE_L.render(ACCENT_COLOR=self.accent_color))
        lbtn.clicked.connect(partial(self.setIndex, 0))
        self.hboxlayout.addWidget(lbtn)
        self.btns.append(lbtn)
        # central buttons.
        index = 1
        for option in options[1:-1]:
            cbtn = self.initBtn(option, role="c")
            cbtn.clicked.connect(partial(self.setIndex, index))
            self.hboxlayout.addWidget(cbtn)
            self.btns.append(cbtn)
            index += 1
        # right button.
        rbtn = self.initBtn(options[-1], role="r")
        rbtn.clicked.connect(partial(self.setIndex, len(options)-1))
        self.hboxlayout.addWidget(rbtn)
        self.btns.append(rbtn)
        
        self.hboxlayout.addStretch(1)
        # radio button title.
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title.setFixedHeight(30)
        self.title.setStyleSheet("background: transparent; color: #fff; font-family: 'Be Vietnam Pro'; font-size: 17px; font-weight: bold;")
        self.title.setText(title)
        # build layout. 
        self.vboxlayout.addWidget(self.title)
        self.vboxlayout.addWidget(self.hbox)
        self.vboxlayout.addStretch(1)
        self.setLayout(self.vboxlayout)

    def setIndex(self, i: int):
        self.deselectBtn(self.i)
        self.i = i
        self.selectBtn(self.i)
        self.indexChanged.emit(self.i)
        self.optionChanged.emit(self.options[self.i])

    def deselectBtn(self, i: int):
        if self.i == 0:
            self.btns[i].setStyleSheet(GRADIENT_RADIO_BTN_STYLE_L.render(ACCENT_COLOR=self.accent_color))
        elif self.i == len(self.btns)-1:
            self.btns[i].setStyleSheet(GRADIENT_RADIO_BTN_STYLE_R.render(ACCENT_COLOR=self.accent_color))
        else:
            self.btns[i].setStyleSheet(GRADIENT_RADIO_BTN_STYLE_C.render(ACCENT_COLOR=self.accent_color))

    def selectBtn(self, i: int):
        if self.i == 0:
            self.btns[i].setStyleSheet(GRADIENT_RADIO_SEL_BTN_STYLE_L.render(ACCENT_COLOR=self.accent_color))
        elif self.i == len(self.btns)-1:
            self.btns[i].setStyleSheet(GRADIENT_RADIO_SEL_BTN_STYLE_R.render(ACCENT_COLOR=self.accent_color))
        else:
            self.btns[i].setStyleSheet(GRADIENT_RADIO_SEL_BTN_STYLE_C.render(ACCENT_COLOR=self.accent_color))

    def getOption(self, i: int):
        return self.options[i]

    def getSelectedOption(self):
        return self.options[self.i]

    def initBtn(self, text: str, role: str="c"):
        btn = QToolButton()
        if role == "l":
            btn.setStyleSheet(GRADIENT_RADIO_BTN_STYLE_L.render(ACCENT_COLOR=self.accent_color))
        elif role == "c":
            btn.setStyleSheet(GRADIENT_RADIO_BTN_STYLE_C.render(ACCENT_COLOR=self.accent_color))
        else:
            btn.setStyleSheet(GRADIENT_RADIO_BTN_STYLE_R.render(ACCENT_COLOR=self.accent_color))
        btn.setText(text)

        return btn

# Gradient control color patch QLineEdit readout.
class GradientControlColorReadout(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(GradientControlColorReadout, self).__init__(parent)


# Control Color Patch.
class GradientControlColorPatch(QWidget):
    valueChanged = pyqtSignal(str)
    def __init__(self, color: str="#000", 
                 parent: Union[None, QWidget]=None):
        super(GradientControlColorPatch, self).__init__(parent)
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        # store the color.
        self.__color = color
        # color patch.
        self.patch = QLabel()
        self.patch.setText("  ")
        self.patch.setFixedWidth(40)
        # readout value.
        self.readout = QLineEdit(color)
        self.readout.setFixedWidth(150)
        self.copyAction = self.readout.addAction(
            FigD.Icon("apps/gradient_creator/copy.svg"), 
            QLineEdit.TrailingPosition
        )
        self.copyAction.triggered.connect(self.copyReadout)
        # style this bitch.
        self.setStyleSheet("""
        QWidget {
            padding: 5px;  
            color: #292929;         
            font-size: 20px;
            font-weight: bold;
            background: white;
        }""")
        self.readout.setStyleSheet("""
        QLineEdit {
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }""")
        self.patch.setStyleSheet("""
        QLabel {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
            background: """+self.__color+""";
        }""")
        self.readout.textChanged.connect(self.setFromReadout)
        # build layout.
        self.hboxlayout.addWidget(self.patch)
        self.hboxlayout.addWidget(self.readout)
        self.setLayout(self.hboxlayout)

    def color(self):
        return self.__color

    def setColor(self, color: str):
        self.__color = color
        self.patch.setStyleSheet("""
        QLabel {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
            background: """+self.__color+""";
        }""")

    def setFromReadout(self):
        """set color from the hex string typed in the readout."""
        value = self.readout.text()
        isvalid = validate_hex_color(value)
        if not isvalid: return
        self.readout.setText(value)
        self.setColor(value)
        self.valueChanged.emit(value)

    def reset(self):
        self.setColor("#000")
        self.readout.setText("#000")

    def copyReadout(self):
        """copy readout value to clipboard."""
        QApplication.clipboard().setText(self.readout.text())
        try:
            statusBar = QApplication.activeWindow().statusbar
        except AttributeError as e:
            statusBar = QApplication.activeWindow().statusBar()
            print(e)
        statusBar.showMessage(f"copied color {self.readout.text()} to clipboard!")
        QTimer.singleShot(1000, statusBar.clearMessage)

# Gradient stop edit button class.
class GradientStopEditBtn(QToolButton):
    def __init__(self, text: str, icon: str, 
                 callback, accent_color: str="green", 
                 parent: Union[None, QWidget]=None):
        super(GradientStopEditBtn, self).__init__(parent)
        self.setText(text)
        self._leave_icon_name = icon
        stem, ext = os.path.splitext(icon)
        self._enter_icon_name = f"{stem}_active{ext}"
        self.setIcon(FigD.Icon(
            os.path.join("apps/gradient_creator", icon)
        ))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 8px;
            font-size: 17px;
            border-radius: 8px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.091 #2e2e2e, stop : 0.182 #333333, stop : 0.273 #383838, stop : 0.364 #3d3d3d, stop : 0.455 #424242, stop : 0.545 #474747, stop : 0.636 #4c4c4c, stop : 0.727 #525252, stop : 0.818 #575757, stop : 0.909 #5d5d5d, stop : 1.0 #626262);
        }
        QToolButton:hover {
            color: #292929;
            background: """+accent_color+""";
        }""")
        self.clicked.connect(callback)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(
            os.path.join(
                "apps/gradient_creator", 
                self._leave_icon_name
            )
        ))
        super(GradientStopEditBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(
            os.path.join(
                "apps/gradient_creator", 
                self._enter_icon_name
            )
        ))
        super(GradientStopEditBtn, self).enterEvent(event)

# Control Stops UI.
class GradientControlStopsPanel(QScrollArea):
    stopListChanged = pyqtSignal(list)
    def __init__(self, accent_color: str="green", 
                 parent: Union[None, QWidget]=None):
        super(GradientControlStopsPanel, self).__init__(parent)
        self.accent_color = accent_color
        self.setStyleSheet("background: transparent;")
        # primary widget.
        self.hbox = QWidget()
        self.hbox.setStyleSheet("""background: transparent;""")
        # primary layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(10)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hbox.setLayout(self.hboxlayout)
        # create 2 color patches.
        self.colorPatch1 = GradientControlColorPatch()
        self.colorPatch2 = GradientControlColorPatch()
        self.colorPatch1.valueChanged.connect(self.signalStopListChange)
        self.colorPatch2.valueChanged.connect(self.signalStopListChange)
        self.patchArray = [self.colorPatch1, self.colorPatch2]
        # add color patch.
        self.addPatchBtn = self.initEditBtn("ADD", "add.svg", self.addPatch)
        # delete last color patch.
        self.delPatchBtn = self.initEditBtn("DELETE", "delete.svg", self.deletePatch)
        # reset color patch.
        self.resetPatchBtn = self.initEditBtn("RESET", "reset.svg", self.reset)
        # build layout.
        self.hboxlayout.addStretch(1)
        self.hboxlayout.addWidget(self.colorPatch1)
        self.hboxlayout.addWidget(self.colorPatch2)
        self.hboxlayout.addWidget(self.addPatchBtn)
        self.hboxlayout.addWidget(self.delPatchBtn)
        self.hboxlayout.addWidget(self.resetPatchBtn)
        self.hboxlayout.addStretch(1)
        # set layout.
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.hbox)
        self.setWidgetResizable(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def signalStopListChange(self):
        stops = []
        numStops = len(self.patchArray)
        for i in range(numStops):
            stop = self.hboxlayout.itemAt(i+1).widget()
            # print(f"stop: {stop}")
            # print(f"color: {stop.color()}")
            stops.append(stop.color())
        self.stopListChanged.emit(stops)

    def addPatch(self):
        """add a color patch at the end."""
        colorPatch = GradientControlColorPatch()
        colorPatch.valueChanged.connect(self.signalStopListChange)
        self.hboxlayout.insertWidget(
            len(self.patchArray)+1, 
            colorPatch
        )
        self.patchArray.append(colorPatch)

    def deletePatch(self):
        """delete the last color patch."""
        if len(self.patchArray) <= 2: return
        i = len(self.patchArray)
        self.hboxlayout.itemAt(i).widget().setParent(None)
        self.patchArray.pop()
        self.signalStopListChange()

    def __len__(self):
        return len(self.patchArray)

    def reset(self):
        self.patchArray[0].reset()
        self.patchArray[1].reset()
        # delete color patches after the first 2.
        for i in range(2, len(self)):
            self.hboxlayout.itemAt(3).widget().setParent(None)
        self.patchArray = self.patchArray[:2]
        self.signalStopListChange()

    def initEditBtn(self, text: str, icon: str, callback):
        """initialize the add and delete stop buttons."""
        btn = GradientStopEditBtn(callback=callback, 
                                  text=text, icon=icon, 
                                  accent_color=self.accent_color)
        return btn

# Coloring UI
class GradientCustomizerUI(QWidget):
    def __init__(self, accent_color: str="green", 
                 parent: Union[None, QWidget]=None):
        super(GradientCustomizerUI, self).__init__(parent)
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(5)
        self.hboxlayout.setContentsMargins(5, 5, 5, 5)
        # create layout.
        self.gradTypeSelector = GradientRadioButton(
            options=["LINEAR", "RADIAL", "CONIC"],
            accent_color=accent_color, title="GRADIENT TYPE"
        )
        self.interpolSelector = GradientRadioButton(
            options=["HCL", "HSB", "HSL"],
            accent_color=accent_color, title="INTERPOLATION"
        )
        self.easingSelector = GradientRadioButton(
            options=["OFF", "ON"],
            accent_color=accent_color, title="EASING"
        )
        # angle slider.
        self.angleSlider = DashSlider(
            "ANGLE", icon="apps/gradient_creator/angle.svg", icon_size=(20,20), 
            minm=0, maxm=360, value=0, accent_color=accent_color)
        self.angleSlider.readout.setAlignment(Qt.AlignRight)
        self.precisionSlider = DashSlider(
            "PRECISION", icon="apps/gradient_creator/precision.svg", icon_size=(20,20), 
            minm=2, maxm=12, value=8, accent_color=accent_color)
        self.precisionSlider.readout.setAlignment(Qt.AlignRight)
        # self.centerXSlider
        # self.centerXSlider.hide()
        # self.centerYSlider
        # self.centerYSlider.hide()
        self.hboxlayout.addStretch(1)
        self.hboxlayout.addWidget(self.gradTypeSelector, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(self.interpolSelector, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(self.angleSlider, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(self.easingSelector, 0, Qt.AlignVCenter)
        self.hboxlayout.addWidget(self.precisionSlider, 0, Qt.AlignVCenter)
        self.hboxlayout.addStretch(1)
        self.setLayout(self.hboxlayout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

# Qt Gradient Visualizer.
class GradientQtVisualizer(QWidget):
    gradGenerated = pyqtSignal(str)
    def __init__(self, grad_type: str="linear", 
                 parent: Union[None, QWidget]=None):
        super(GradientQtVisualizer, self).__init__(parent)
        self.grad_type = grad_type
        # patch widget.
        self.patch = QWidget()
        self.patch.setStyleSheet("""
        QWidget {
            background: #000;
            border-radius: 10px;
        }""")
        # create vertical layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        # build layout.
        self.vboxlayout.addWidget(self.patch)
        # set layout.
        self.setLayout(self.vboxlayout)
        # angle, cx, cy.
        self.angle = 0
        self.cx = 0
        self.cy = 0 

    def update(self, stops: List[str]):
        grad = ""
        if self.grad_type == "linear":
            offset = 0
            diff = 1/len(stops)
            grad += "qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0,"
            for stop in stops:
                grad += f" stop: {offset} {stop},"
                offset += diff
        grad = grad[:-1]
        grad += ")"
        # print(grad)
        self.patch.setStyleSheet("""
        QWidget {
            background: """+grad+""";
            border-radius: 10px;
        }""")
        self.gradGenerated.emit(grad)

# CSS & SVG Gradient Visulaizer.
class GradientCSSSVGVisualizer(QWidget):
    pass

# Gradient Creator for fig-dash.
class DashGradientCreator(QWidget):
    def __init__(self, accent_color: str="green", 
                 parent: Union[None, QWidget]=None):
        super(DashGradientCreator, self).__init__(parent)
        # vertical layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setSpacing(5)
        self.vboxlayout.setContentsMargins(5, 5, 5, 5)
        # Qt gradient visualizer
        self.qt_visualizer = GradientQtVisualizer()
        self.qt_visualizer.setFixedHeight(100)
        # self.qt_visualizer.gradGenerated.connect()
        # UI for adding, deleting and editing gradient stops.
        self.grad_stops_ui = GradientControlStopsPanel(
            accent_color=accent_color
        )
        self.grad_stops_ui.stopListChanged.connect(self.qt_visualizer.update)
        self.customizer_ui = GradientCustomizerUI(
            accent_color=accent_color
        )
        self.customizerArea = QScrollArea()
        self.customizerArea.setObjectName("CustomizerArea")
        self.customizerArea.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
        }""")
        self.customizerArea.setAttribute(Qt.WA_TranslucentBackground)
        self.customizerArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.customizerArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.customizerArea.setWidget(self.customizer_ui)
        self.customizerArea.setWidgetResizable(True)
        # build layout.
        self.vboxlayout.addWidget(self.qt_visualizer)
        self.vboxlayout.addWidget(self.grad_stops_ui)
        self.vboxlayout.addWidget(self.customizerArea)
        self.vboxlayout.addStretch(1)
        self.setLayout(self.vboxlayout)

def test_gradient_creator():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    icon = AppIconMap["gradient_creator"]
    title = " ".join(AppTitleMap["gradient_creator"].split())
    accent_color = AccentColorMap["gradient_creator"]
    gradient_creator = DashGradientCreator(accent_color=accent_color)
    accent_color = TitleBarAccentColorMap["gradient_creator"]
    window = wrapFigDWindow(gradient_creator, size=(20,20), width=700,
                            title=title, height=500,  name="gradient_creator",
                            icon=icon, accent_color=accent_color)
    window = styleWindowStatusBar(window)
    window.show()
    app.exec()

def launch_gradient_creator(app):
    icon = AppIconMap["gradient_creator"]
    title = " ".join(AppTitleMap["gradient_creator"].split())
    accent_color = AccentColorMap["gradient_creator"]
    gradient_creator = DashGradientCreator(accent_color=accent_color)
    accent_color = TitleBarAccentColorMap["gradient_creator"]
    window = wrapFigDWindow(gradient_creator, size=(20,20), width=700,
                            title=title, height=500, name="gradient_creator",
                            icon=icon, accent_color=accent_color)
    window = styleWindowStatusBar(window)
    window.show()

    return window


if __name__ == "__main__":
    test_gradient_creator()