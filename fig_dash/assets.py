#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Asset management for ScriptO'''
import os
from pathlib import Path
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QFont


class AssetManager:
    '''A class to bundle path completion resources for fig'''
    def __init__(self, resource_dir: str=""):
        self.dir = resource_dir
        self.reset(resource_dir)

    def reset(self, resource_dir: str):
        self.icon_dir = os.path.join(resource_dir, "icons")
        self.font_dir = os.path.join(resource_dir, "fonts")
        self.style_dir = os.path.join(resource_dir, "style")
        self.static_dir = os.path.join(resource_dir, "static")

    def __call__(self, resource_dir: str):
        self.dir = resource_dir
        self.reset(resource_dir)

    def icon(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.icon_dir, path)

    def font(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.font_dir, path)

    def asset(self, path: str) -> str:
        '''return absolute path of an asset'''
        return os.path.join(self.resource_dir, path)

    def static(self, path: str) -> str:
        '''give relative path and get absolute static path.'''
        return os.path.join(self.static_dir, path)

    def staticUrl(self, path: str) -> QUrl:
        '''local url given static path'''
        filePath = self.static(path)

        return QUrl.fromLocalFile(filePath)

    def Icon(self, name:str) -> QIcon :
        '''return QIcon'''
        icon_path = self.icon(name)
        icon = QIcon(icon_path)

        return icon

    def Font(self, name: str) -> QFont :
        '''return QFont'''
        font_path = self.icon(name)
        font = QFont(font_path)

        return font


FigD = AssetManager()
if __name__ == "__main__":
    FigD = AssetManager("resources")
    print(FigD.icon("titlebar/close.png"))