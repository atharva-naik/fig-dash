#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
from pathlib import Path
LINUX_APP_DEFAULTS_PATH = "/usr/share/applications/defaults.list"
DESKTOP_FILES_FOLDERS = [
    os.path.expanduser("~/.local/share/applications/"),
    "/usr/share/applications/"
]
APP_ICONS_FOLDERS = [
    os.path.expanduser("~/.local/share/icons"),
    os.path.expanduser("/usr/share/icons/hicolor"),
]
APP_INFO_CACHE_DIR = os.path.expanduser("~/.fig_dash")
os.makedirs(APP_INFO_CACHE_DIR, exist_ok=True)

class IconMap:
    '''map icons to their stems'''
    def __init__(self, folders: str=APP_ICONS_FOLDERS):
        self.paths = folders
        self._map = {}
        self._cache_path = os.path.join(
            APP_INFO_CACHE_DIR,
            "icons.json"
        )
        s = time.time()
        if os.path.exists(self._cache_path):
            secs = time.time()-os.path.getmtime(self._cache_path) 
            self._map = json.load(open(self._cache_path))
            if secs > 60*60:
                # refresh icons.json every hour.
                os.remove(self._cache_path)
        else:
            for path in self.paths:
                self._load(path)
            with open(self._cache_path, "w") as f:
                json.dump(
                    self._map, 
                    f,indent=4
                )
        print(f"loaded icons in {time.time()-s}s")

    def __getitem__(self, key: str):
        '''get icon: try .png, .svg, absolute filepath.'''
        return self._map.get(
            key+".png", 
            self._map.get(
                key+".svg",
                self._map.get(
                    key,
                    ["default.svg"]
                )
            )
        )
    # def load(self, folder):
    #     for file in os.listdir(folder):
    #         path = os.path.join(self.path, file)
    #         if os.path.isfile(path):
    #             self.add(file, self.path)
    #         elif os.path.isdir(path):
    #             print(path)
    #             # assuming folder.
    #             self._load(path)
    def _load(self, folder: str):
        '''load subfolder for icons.'''
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            if os.path.isfile(path):
                self.add(file, folder)
            elif os.path.isdir(path):
                self._load(path)

    def add(self, file: str, folder: str):
        '''add icon entry using file and containing folder.'''
        stem = Path(file).stem
        name = Path(file).name
        path = os.path.join(folder, file)
        try:
            self._map[stem].append(path)
        except KeyError:
            self._map[stem] = [path]
        try:
            self._map[name].append(path)
        except KeyError:
            self._map[name] = [path]
        try:
            self._map[path].append(path)
        except KeyError:
            self._map[path] = [path]
FigDIconMap = IconMap()


class DesktopFile:
    '''represents desktop file entries for Linxu Files.'''
    def __init__(self, name, folders=DESKTOP_FILES_FOLDERS):
        self.folders = folders
        if name.endswith(".desktop"):
            self.name = name
        else: self.name = name+".desktop"
        self.app_name, _ = os.path.splitext(self.name)
        self.paths = [
            os.path.join(folder, self.name) for folder in folders
        ]
        self._content = None
        self._data = {}

    def __getitem__(self, key: str):
        '''fetch data loaded from the desktop file.'''
        return self._data.get(key, key.upper()+"_NOT_FOUND")

    def getIcons(self):
        '''fetch the icon from the icon map'''
        return FigDIconMap[self['Icon']]

    def getIcon(self):
        '''fetch the icon from the icon map'''
        return FigDIconMap[self['Icon']][0]

    def read(self):
        '''read the desktop file if it exists.'''
        # check if file exists to avoid exceptions
        for path in self.paths:
            if not os.path.exists(path): 
                print(f"FileNotFoundError: {path}")
                continue
            else:
                with open(path) as f:
                    for line in f:
                        line = line.strip()
                        # skip line declaring the desktop file.
                        if line in ["[Desktop Entry]", "", "[Desktop Action new-window]", "[Desktop Action new-document]"]:
                            continue
                        key, value = line.split("=")
                        # store data in key value pairs.
                        key = key.strip()
                        value = value.strip().strip(";")
                        # split mimetypes by ';' to get a list.
                        if key == "MimeType":
                            value = value.split(";")
                        self._data[key] = value
                break

    def __str__(self):
        '''print format'''
        serialized = ""
        for key, value in self._data.items():
            serialized += f"{key}: {value}\n"

        return serialized.strip()


class MimeTypeDefaults:
    def __init__(self, linux_defaults=LINUX_APP_DEFAULTS_PATH):
        import platform
        self._mime_map = {}
        self.os_dist = platform.system()
        if self.os_dist == "Linux":
            for line in open(linux_defaults):
                if line.strip() == "[Default Applications]": continue
                mimetype, apps = line.strip().split("=")
                self._mime_map[mimetype] = apps.strip().split(";")

    def __getitem__(self, key: str):
        '''get the default'''
        return self._mime_map.get(key)

    def __call__(self, key: str):
        '''get the entire list.'''
        return self._mime_map.get(key, [])