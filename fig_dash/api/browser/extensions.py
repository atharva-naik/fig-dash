#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::api::browser")
import os
import sys
import json
import jinja2
CHROME_EXTENSIONS_FOLDER = os.path.expanduser("~/.config/google-chrome/Default/Extensions")


class ManifestTemplate:
    def __init__(self, path: str):
        self.path = path
        self.string = open(path).read()

    def populate(self, locale):
        for k,v in locale.items():
            if isinstance(v, dict):
                self.string = self.string.replace(k, v['message'])
            elif isinstance(v, str):
                self.string = self.string.replace(k, v)
        manifest = json.loads(self.string)

        return manifest


class ExtensionVersion:
    '''convert extension version str into a comparable numerical type.'''
    def __init__(self, version_str):
        version_str, underscore_ind = version_str.split('_')
        self.underscore_ind = int(underscore_ind)
        self.version_tuple = tuple(int(v) for v in version_str.split('.')+[underscore_ind])
        self.version_strs = tuple(str(v) for v in version_str.split('.')+[str(underscore_ind)])

    def version_str(self):
        return ".".join(self.version_strs[:-1])+f"_{self.underscore_ind}"

    def __str__(self):
        return str(self.version_tuple)

    def __repr__(self):
        return str(self.version_tuple)

    def __lt__(self, other):
        return self.version_tuple < other.version_tuple

    def __eq__(self, other):
        return self.version_tuple == other.version_tuple

    def __gt__(self, other):
        return self.version_tuple == other.version_tuple


class ExtensionManager:
    '''class to load and manage extensions.'''
    def __init__(self, folder=CHROME_EXTENSIONS_FOLDER, **args):
        self.extensions = []
        for folder in os.listdir(folder):
            if folder == "Temp": continue
            path = os.path.join(CHROME_EXTENSIONS_FOLDER, folder)
            self.extensions.append(path)
        self.extData = []
        # to load lang specific details from locale.
        self.lang = args.get("lang", "en") 

    def loadExtension(self, i: int):
        path = self.extensions[i]
        versions = [] 
        for version in os.listdir(path):
            versions.append(ExtensionVersion(version))
        latest_version = sorted(versions, reverse=True)[0]
        self.extData[i]["path"] = os.path.join(path, latest_version.version_str())
        for version in versions:
            self.extData[i]["all_paths"] = os.path.join(path, version.version_str())
        self.extData[i]["version_obj"] = version
        manifest_path = os.path.join(
            self.extData[i]["path"],
            "manifest.json",
        )
        locale_dir = os.path.join(
            self.extData[i]["path"],
            "_locales",
        )
        if os.path.exists(locale_dir):
            all_langs = [lang for lang in os.listdir(locale_dir)]
        else: all_langs = []
        locale_path = os.path.join(locale_dir, "en/messages.json")
        if not os.path.exists(locale_path):
            locale_path = ""        
        all_locale_paths = [os.path.join(locale_dir, lang+"/messages.json") for lang in all_langs]
        locale = self.loadLocale(locale_path)
        locale = {key: value["message"] for key, value in locale.items()}
        manifest = ManifestTemplate(
            manifest_path
        ).populate(locale)

        self.extData[i]["locale"] = locale
        self.extData[i]["all_langs"] = all_langs
        self.extData[i]["locale_dir"] = locale_dir
        self.extData[i]["locale_path"] = locale_path
        self.extData[i]["all_locale_paths"] = all_locale_paths
        # print(manifest)
        self.extData[i]["manifest_path"] = manifest_path
        self.extData[i]["manifest"] = manifest
        self.extData[i]["name"] = manifest["name"]
        self.extData[i]["icons"] = []
        self.extData[i]["version"] = manifest["version"]
        self.extData[i]["permissions"] = manifest.get("permissions",[])
        self.extData[i]["description"] = manifest["description"]
        self.extData[i]["update_url"] = manifest["update_url"]

    def loadLocale(self, locale_path: str):
        if os.path.exists(locale_path):
            locale = {}
            pre_locale = json.load(open(locale_path))
            # print(locale)
            for key, value in pre_locale.items():
                # print(f"__MSG_{key}__")
                locale[f"__MSG_{key}__"] = value
        
            return locale
        else:
            return {}

    def locale(self, index: int):
        return self.extData[index]["locale"]

    def manifest(self, index: int):
        return self.extData[index]["manifest"]

    def getVersion(self, index: int):
        return self.extData[index]["version"]

    def getPermissions(self, index: int):
        return self.extData[index]["permissions"]

    def getDescription(self, index: int):
        return self.extData[index]["description"]

    def getUpdateUrl(self, index: int):
        return self.extData[index]["update_url"]

    def toString(self, index: int):
        name = self.getName(index)
        icons = self.getIcons(index)
        version = self.getVersion(index)
        update_url = self.getUpdateUrl(index)
        description = self.getDescription(index)
        permissions = self.getPermissions(index)

        return f"""name: {name}
version: {version}
icons: {icons}
description: {description}
update_url: {update_url}
permissions: {permissions}"""

    def __call__(self, i: int):
        return self.getData(i)

    def print(self, index: int):
        print(self.toString(index))

    def getName(self, index: int):
        return self.extData[index]["name"]

    def getIcons(self, index: int):
        return self.extData[index]["icons"]

    def getData(self, index: int):
        return self.extData[index]

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return len(self.extensions)

    def __getitem__(self, key):
        return self.extensions[key]

    def load(self):
        for i in range(len(self)):
            self.extData.append({})
            self.loadExtension(i)