#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2
import platform
from typing import Union
# Qt5 imports.
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QToolButton
# fig-dash import.
from fig_dash.assets import FigD
from fig_dash.api.system.audio import PulseController


volume_slider_widget_style = '''
QWidget {
    border: 0px;
    color: #fff;
    background: transparent;
}
QLineEdit {
    color: #fff;
    width: 50px;
    text-align: center;
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #292929, stop: 0.5 #484848, stop: 1 #292929);
}'''
volume_slider_style = jinja2.Template("""
QSlider {
    min-width: 250px;
}
QSlider::handle:horizontal {
    width: 20px;
    height: 20px;
    border: 0px;
    padding: 0px;
    margin: -5px 0px;
    border-radius: 9px; 
    /* background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #aaa, stop: 0.5 #484848, stop: 1 #aaa); */
    background: qradialgradient(cx: 0, cy: 0, radius: 1, fx: 2, fy: 2, stop: 0 #292929, stop: 1 #aaa);
}
QSlider::groove:horizontal {
    height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
    /* background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4); */
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #292929, stop: 0.8 {{ BACKGROUND_COLOR }}, stop: 1 #eee);
    border-radius: 3px;
}""")
class VolumeSlider(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(VolumeSlider, self).__init__(parent)
        # attach the backend.
        if platform.system() == 'Linux':
            self.backend = PulseController()
        self.setObjectName("VolumeSlider")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # widgets.
        self.label = QLabel("Adjust Volume")
        self.label.setStyleSheet("""
        QLabel {
            font-size: 20px;
        }""")
        self.label.setAlignment(Qt.AlignCenter)
        self.sliderWidget = self.initSlider()
        self.formWidget = self.initForm()
        # add widgets to the layout.
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.sliderWidget)
        self.layout.addWidget(self.formWidget)
        self.setLayout(self.layout)
        self.setStyleSheet(volume_slider_widget_style)

    def updateVolume(self, value):
        # convert scale
        volume = 1.50*(value/99) # ranges from 0 to 120
        displayVolume = int(100*volume)
        # print("volume:", displayVolume)
        self.backend.set_volume(volume)
        self._readout.setText(f"{displayVolume}  ")
        self._form.setText(str(round(100*volume, 2)))
        self.setSliderColor(volume)
        self.setVolumeIcon(volume)

    def setVolume(self):
        try: 
            volume = float(self._form.text())
            self.backend.set_volume(volume/150)
            self._slider.setValue(int(99*(volume/150)))
            # self._readout.setText(f"{volume:.0f}  ")
            # self.setSliderColor(volume/150)
            # self.setVolumeIcon(volume/150)
        except ValueError:
            return

    def setSliderColor(self, volume: float):
        color = self.getSliderColor(volume)
        # print(color)
        self._slider.setStyleSheet(volume_slider_style.render(
            BACKGROUND_COLOR=color,
        ))

    def setVolumeIcon(self, volume: float):
        icon = self.getVolumeIcon(volume)
        self._motif.setIcon(icon)

    def getVolumeIcon(self, volume: float):
        if volume < 0.5:
            return FigD.Icon("system/audio/low.svg") 
        elif volume > 1:
            return FigD.Icon("system/audio/medium.svg")
        else:
            return FigD.Icon("system/audio/high.svg")

    def getSliderColor(self, volume: float):
        if volume < 0.5:
            x = volume/0.5
            r = 255
            g = 0*(1-x) + 255*x
            b = 0
            return f"rgb({r}, {g}, {b})"
        elif volume < 1:
            x = (volume-0.5)/0.5
            r = 255*(1-x)+0*x
            g = 255
            b = 0
            return f"rgb({r}, {g}, {b})"
        else:
            x = (volume-1)/0.5
            r = 0
            g = 255*(1-x)+0*x
            b = 255*x+0*(1-x)
            return f"rgb({r}, {g}, {b})"

    def backendToSlider(self, volume: float):
        '''converts volume from backend to slider scale'''
        volume = min(volume, 1.5)
        return int(99*(volume/1.5))

    def initForm(self):
        '''form/ lineedit to set volume'''
        formContainer = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self._form = QLineEdit()
        sink_volumes = self.backend.get_volume()
        self._form.setText(str(round(100*sink_volumes[0], 2)))
        self._form.setAlignment(Qt.AlignCenter)
        self._form.returnPressed.connect(self.setVolume)
        self._form.setMaximumWidth(100)

        # add widgets to form container.
        label = QLabel(" set")
        label.setAlignment(Qt.AlignCenter)
        # layout.addWidget(label)
        layout.addWidget(self._form)
        formContainer.setLayout(layout)

        return formContainer

    def initMotif(self):
        motif = QToolButton(self)
        motif.setIconSize(QSize(20,20))

        return motif

    def initSlider(self):
        '''create the slider widget.'''
        sliderContainer = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self._slider = QSlider(self)
        self._slider.setOrientation(Qt.Horizontal)
        sink_volumes = self.backend.get_volume()
        self._slider.setValue(self.backendToSlider(sink_volumes[0]))
        self._slider.valueChanged.connect(self.updateVolume)
        
        self._motif = self.initMotif()
        self._readout = QLabel(f"{100*sink_volumes[0]:.0f}  ")

        # add slider widgets.
        layout.addWidget(self._motif)
        layout.addWidget(self._slider)
        layout.addWidget(self._readout)
        sliderContainer.setLayout(layout)
        
        self.setSliderColor(sink_volumes[0])
        self.setVolumeIcon(sink_volumes[0])

        return sliderContainer

def test_slider():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    volume_slider = VolumeSlider()
    volume_slider.show()
    app.exec()


if __name__ == '__main__':
    test_slider()