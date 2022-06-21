#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Asset management for FigD'''
from fig_dash import FigDLoad
FigDLoad("fig_dash::ui::assets")

import os
import jinja2
import logging
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QFont


class AssetManager:
    '''A class to bundle path completion resources for fig'''
    def __init__(self, resource_dir: str="~/GUI/fig-dash/resources"):
        self.temp_file_ctr = 0
        resource_dir = os.path.expanduser(resource_dir)
        # print(f"reading resources from: {resource_dir}")
        self.ResourcePath = resource_dir
        self.ResourceUrl = QUrl.fromLocalFile(self.ResourcePath)
        self.dir = resource_dir
        self.reset(resource_dir)
        # initialize logger and allow colored logs.
        self.logger = logging.getLogger(__name__)
        import coloredlogs
        coloredlogs.install(level="debug", logger=self.logger)
        
    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def reset(self, resource_dir: str):
        self.icon_dir = os.path.join(resource_dir, "icons")
        self.font_dir = os.path.join(resource_dir, "fonts")
        self.style_dir = os.path.join(resource_dir, "style")
        self.theme_dir = os.path.join(resource_dir, "theme")
        self.static_dir = os.path.join(resource_dir, "static")
        self.locale_dir = os.path.join(resource_dir, "locales")
        self.temp_foldir = os.path.join(self.static_dir, "TEMP_FILES")
        self.wallpaper_dir = os.path.join(resource_dir, "wallpapers")
        self.wallpaper_paths = []
        for category in os.listdir(self.wallpaper_dir):
            root = os.path.join(self.wallpaper_dir, category)
            for filename in os.listdir(root):
                self.wallpaper_paths.append(os.path.join(
                    self.wallpaper_dir, 
                    category, filename
                ))
        # set constants.
        self.TempURLPath = QUrl.fromLocalFile(self.static_dir).toString()

    def __call__(self, resource_dir: str):
        self.dir = resource_dir
        self.reset(resource_dir)

    def wallpaper(self, path: str) -> str:
        '''return real absolute path of wallpaper.'''
        return os.path.join(self.wallpaper_dir, path)

    def wallpapers(self, i: int):
        '''return a list of all wallpapers.'''
        return self.wallpaper_paths[i]

    def icon(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.icon_dir, path)

    def font(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.font_dir, path)

    def asset(self, path: str) -> str:
        '''return absolute path of an asset'''
        return os.path.join(self.resource_dir, path)

    def theme(self, path: str) -> str:
        '''return absolute path of theme file'''
        return os.path.join(self.theme_dir, path)

    def locale(self, path: str) -> str:
        """[summary]
        get full path of a locale based asset.
        Args:
            path (str): [description] relative path of local asset

        Returns:
            str: [description] full path of local asset
        """
        return os.path.join(self.locale_dir, path)

    def static(self, path: str, **params) -> str:
        '''give relative path and get absolute static path.'''
        template_path = os.path.join(self.static_dir, path)
        with open(template_path) as f:
            template = jinja2.Template(f.read())
            html = template.render(**params)
        with open("/tmp/fig_dash.rendered.content.html", "w") as f:
            f.write(html)

        return QUrl.fromLocalFile("/tmp/fig_dash.rendered.content.html")

    def staticUrl(self, path: str) -> QUrl:
        '''local url given static path'''
        filePath = os.path.join(self.static_dir, path)

        return QUrl.fromLocalFile(filePath).toString()

    def createTempUrl(self, content: str) -> QUrl:
        os.makedirs(self.temp_foldir, exist_ok=True)
        tempPath = os.path.join(
            self.temp_foldir,
            f"{self.temp_file_ctr}.html"
        )
        self.temp_file_ctr += 1
        with open(tempPath, "w") as f:
            f.write(content)
        
        return QUrl.fromLocalFile(tempPath)

    def createTempPath(self, content: str, ext: str="html") -> str:
        os.makedirs(self.temp_foldir, exist_ok=True)
        tempPath = os.path.join(
            self.temp_foldir,
            f"{self.temp_file_ctr}.{ext}"
        )
        self.temp_file_ctr += 1
        with open(tempPath, "w") as f:
            f.write(content)
        
        return tempPath

    def __del__(self):
        '''delete temporary file.'''
        if self.temp_foldir.endswith("TEMP_FILES"):
            print(f"deleting temp_foldir: {self.temp_foldir}")
        # try: shutil.rmtree(self.temp_dir)
        # except FileNotFoundError: pass
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

# asset manager.
FigD = AssetManager()
if __name__ == "__main__":
    FigD = AssetManager("resources")
    tempURL = FigD.createTempUrl("lol wow")
    print(FigD.icon("titlebar/close.png"))