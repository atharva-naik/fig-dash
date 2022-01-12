#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSlot, pyqtSignal, QObject
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.api.system.notifs.desktop import desktop_notify


FigDesktopNotifJS = r'''
class FigDesktopNotif {
    constructor(message, title="", icon="") {
        this.title = title;
        this.icon = icon;
        this.message = message
    }
    log() {
        // log desktop notification details.
        console.log(`${this.icon}${this.title}\n${this.message}`);
    }
    send() {
        // send desktop notification.
        var icon = this.icon;
        var title = this.title;
        var message = this.message;
        new QWebChannel(qt.webChannelTransport, function(channel) {
            var systemHandler = channel.objects.systemHandler;
            systemHandler.sendDesktopNotif(message, title, icon);
        });
    }
}'''
FigFileManagerJS = r'''
class FigFileOpResult {
    constructor(path, op="Unspecified") {
        this.path = path;
        this.op = op;
        this.complete = false;
    }
    isComplete() {
        return this.complete;
    }
}
class FigFileExists extends FigFileOpResult {
    constructor(path) {
        super(path, "FileExists");
    }
    set(file_exists) {
        this.complete = true;
        this.exists = file_exists;
    }
}
class FigFileManager {
    constructor(root) {
        this.root = root;
    }
    exists(path) {
        var opResult = new FigFileExists(path);
        new QWebChannel(qt.webChannelTransport, function(channel) {
            var systemHandler = channel.objects.systemHandler;
            systemHandler.receiveFileManagerPathExists(path, function(pathExists) {
                opResult.set(pathExists);
            });
        });

        return opResult;
    }
}'''+f'''
var FigFileRoot="{os.path.expanduser('~')}"; '''


class SystemHandler(QObject):
    def __init__(self):
        super(SystemHandler, self).__init__()
        self.js_sources = {
            "FIG_FILE_MANAGER_JS": FigFileManagerJS,
            "FIG_DESKTOP_NOTIF_JS": FigDesktopNotifJS,
        }

    def connectChannel(self, channel):
        self.channel = channel
        self.channel.registerObject("systemHandler", self)

    @pyqtSlot(str, str, str)
    def sendDesktopNotif(self, message: str, 
                         title: str, icon: str):
        # icon = FigD.icon(icon)
        desktop_notify(
            msg=message, 
            title=title, 
            icon=icon
        )

    @pyqtSlot(str, result=bool)
    def receiveFileManagerPathExists(self, path):
        print(os.path.exists(path))
        return os.path.exists(path)