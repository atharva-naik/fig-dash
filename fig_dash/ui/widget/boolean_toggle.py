#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::widget::boolean_toggle")
# qtwidgets import.
import sys
from typing import *
# PyQt5 imports
from PyQt5.QtGui import QColor, QIcon, QPixmap, QBrush, QPaintEvent, QPen, QPainter, QLinearGradient, QRadialGradient, QConicalGradient
from PyQt5.QtCore import Qt, QSize, QPoint, QPointF, QRectF, QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QHBoxLayout, QVBoxLayout

# toggle box.
class Toggle(QCheckBox):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    def __init__(self, parent=None, bar_color: Union[QColor, int]=Qt.gray,
                 checked_color: str="#00B0FF", handle_color: Union[QColor, int]=Qt.white):
        super(Toggle, self).__init__(parent)
        self._bar_text = "off"
        print(f"\x1b[34;1mbar_color:\x1b[0m {bar_color}")
        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        def qt_grad_from_str(qt_grad_str: str) -> Union[QLinearGradient, QRadialGradient, QConicalGradient]:
            qt_grad_str = qt_grad_str.strip()
            if qt_grad_str.startswith("qlineargradient"):
                grad_class = QLinearGradient
            elif qt_grad_str.startswith("qradialgradient"):
                grad_class = QRadialGradient
            elif qt_grad_str.startswith("qconicalgradient"):
                grad_class = QConicalGradient
            qt_grad = grad_class()
            for part in qt_grad_str.split("stop")[1:]:
                subpart = part.split("#")
                stop = float(subpart[0].replace(":","").replace(",",""))
                color = "#"+subpart[1].replace(":","").replace(",","").strip()
                qt_grad.setColorAt(stop, QColor(color))

            return qt_grad
        if isinstance(bar_color, str):
            self._bar_brush = QBrush(qt_grad_from_str(bar_color))
            self._bar_brush.setStyle(Qt.BrushStyle.LinearGradientPattern)
        elif isinstance(bar_color, int) or isinstance(bar_color, QColor):
            self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())
        print(f"bar checked brush: {QColor(checked_color).lighter().name()}")
        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))
        # Setup the rest of the widget.
        # self.setContentsMargins(8, 0, 8, 0)
        self.setContentsMargins(12, 0, 12, 0)
        self._handle_position = 0
        self.stateChanged.connect(self.handleStateChanged)

    def sizeHint(self):
        return QSize(45, 37)
        # return QSize(52, 40)
        # return QSize(58, 45)
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
        barRect.moveCenter(contRect.center())
        p.drawText(barRect, Qt.AlignCenter, self._bar_text)
        rounding = barRect.height() / 2
        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)
        p.end()

    @pyqtSlot(int)
    def handleStateChanged(self, value):
        self._handle_position = 1 if value else 0

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()

# Animated toggle button.
class AnimatedToggle(Toggle):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    def __init__(self, *args, pulse_unchecked_color: str="#44999999",
                 pulse_checked_color: str="#4400B0EE", **kwargs):
        self._pulse_radius = 0
        super(AnimatedToggle, self).__init__(*args, **kwargs)
        # property animation for handle position.
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms
        # property animaton for pulse radius.
        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)
        # sequentially chain/group animations.
        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        pulse_checked_color = QColor(pulse_checked_color).lighter()
        pulse_checked_color.setAlphaF(0.7)
        print(f"pulse checked color: {pulse_checked_color.name()}")
        self._pulse_checked_animation = QBrush(pulse_checked_color)

    @pyqtSlot(int)
    def handleStateChanged(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2
        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position
        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(QPointF(xPos, barRect.center().y()), handleRadius, handleRadius)
        p.end()

# boolean toggle widget with label.
class BooleanToggleBtn(QWidget):
    def __init__(self, parent=None, pulse_checked_color: str="#44FFB000", 
                 checked_color: str="#FFB000", width: int=65, text: str="", 
                 icon: Union[QIcon, str, None]=None, orient: str="", **kwargs) -> None:
        super(BooleanToggleBtn, self).__init__(parent)
        self.toggleBtn = AnimatedToggle(
            pulse_checked_color=pulse_checked_color,
            checked_color=checked_color, **kwargs, 
        )
        text = kwargs.get("text")
        icon = kwargs.get("icon")
        orient = kwargs.get("orient", "horizontal")
        if orient == "vertical":
            self.boxlayout = QVBoxLayout()
        elif orient == "horizontal":
            self.boxlayout = QHBoxLayout()
        if icon:
            self.iconLabel = QIcon()
            if isinstance(icon, str):
                self.iconPixmap = QPixmap(icon)
            elif isinstance(icon, QIcon):
                self.iconPixmap = icon.pixmap(20,20)
            self.iconLabel.setPixmap(self.iconPixmap)
            self.boxlayout.addWidget(self.iconLabel, 0, Qt.AlignCenter)
        self.boxlayout.setContentsMargins(0, 0, 0, 0)
        self.boxlayout.setSpacing(0)
        self.boxlayout.addWidget(self.toggleBtn, 0, Qt.AlignCenter)
        if text:
            self.label = QLabel()
            self.label.setText(text)
            self.boxlayout.addWidget(self.label, 0, Qt.AlignCenter)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setWordWrap(True)
        self.boxlayout.addStretch(1)
        self.toggleBtn.setFixedWidth(width)
        self.setLayout(self.boxlayout)
# # test boolean toggle button.
# def test_boolean_toggle():
#     from fig_dash.ui import FigDAppContainer, wrapFigDWindow
#     FigD("/home/atharva/GUI/fig-dash/resources")
#     accent_color = "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #9f6e00, stop : 0.091 #a77400, stop : 0.182 #b07a00, stop : 0.273 #b87f00, stop : 0.364 #c18500, stop : 0.455 #c98b00, stop : 0.545 #d29100, stop : 0.636 #db9700, stop : 0.727 #e49e00, stop : 0.818 #eda400, stop : 0.909 #f6aa00, stop : 1.0 #ffb000)"
#     app = FigDAppContainer(sys.argv)
#     boolean_toggle = BooleanToggleBtn(text="test", icon="/home/atharva/GUI/spectrum_icons/icons/Smock_IdentityService_18_N.svg", bar_color=QColor("#d6d6d6"))
#     widget = QWidget()
#     layout = QVBoxLayout()
#     layout.setSpacing(0)
#     layout.setContentsMargins(0, 0, 0, 0)
#     layout.addWidget(boolean_toggle)
#     widget.setLayout(layout)
#     # create FigD window.
#     window = wrapFigDWindow(
#         widget, icon="fig.svg",
#         accent_color=accent_color, 
#         title="Boolean Toggle",
#         height=200, width=700,
#     )
#     window.show()
#     # launch app.
#     app.exec()
# main section.
if __name__ == "__main__":
    pass
    # test_boolean_toggle()
# bar_color = "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #808080, stop : 0.091 #878787, stop : 0.182 #8f8f8f, stop : 0.273 #979797, stop : 0.364 #9e9e9e, stop : 0.455 #a6a6a6, stop : 0.545 #aeaeae, stop : 0.636 #b6b6b6, stop : 0.727 #bebebe, stop : 0.818 #c6c6c6, stop : 0.909 #cecece, stop : 1.0 #d6d6d)"