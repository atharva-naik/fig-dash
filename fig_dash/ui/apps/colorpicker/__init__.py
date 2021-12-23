#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from PyQt5.QtWidgets import QApplication
# import color piicker UI
from fig_dash.ui.apps.colorpicker.colorpicker import ColorPicker


def LaunchGPick():
    '''Launch gpick.'''
    try: 
        subprocess.call(['gpick1'])
        return True
    except FileNotFoundError: 
        print("gpick not installed")
        return False

def LaunchQtColorPicker():
    app = QApplication([])
    cp = ColorPicker(useAlpha=True, lightTheme=False)
    default_color = (255,175,24,80)
    picked = cp.getColor(default_color)
    
    return picked

def GetColorPicker():
    if not LaunchGPick():
        print("defaulting to inferior qt-colorpicker")
        return LaunchQtColorPicker()

def test_colorpicker():
    app = QApplication([])
    my_color_picker = ColorPicker(useAlpha=True)
    my_color_picker_light = ColorPicker(lightTheme=True)

    old_color = (255,255,255,50)
    picked_color = my_color_picker.getColor(old_color)
    print(picked_color)

    old_color = (255,0,255)
    picked_color = my_color_picker_light.getColor(old_color)
    print(picked_color)
    # Don't have your color in RGB format?
    my_color = (50, 50, 100, 60) # HSV Color in percent
    old_color = my_color_picker.hsv2rgb(my_color)
    picked_color = my_color_picker.rgb2hsv(my_color_picker.getColor(old_color))
    print(picked_color)


if __name__ == '__main__':
    test_colorpicker()
