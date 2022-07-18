#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import *
from functools import partial
from PyQt5.QtCore import QObject, QThread, pyqtSignal

# worker with all the necessary signals and the vlc media player instance.
class MusicPlayerBackendThread(QThread):
    pass

class MusicPlayerBackendWorker(QObject):
    finished = pyqtSignal()
    def __init__(self, path, **args):
        super(MusicPlayerBackendWorker, self).__init__()
        self.path = path
        self.player = None
        self.autoPlay = args.get("autoplay", True)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def close(self):
        """close the function"""
        self.finished.emit()

    def init(self):
        import vlc
        self.player = vlc.MediaPlayer(self.path)
        if self.autoPlay: self.player.play()

# the backend (headless) portion for JukeBox.
# depends on VLC media player. 
class MusicPlayerBackend:
    def __init__(self):
        self.threads: List[MusicPlayerBackendThread] = []
        self.workers: List[MusicPlayerBackendWorker] = []

    def play(self, i: int):
        self.workers[i].play()

    def pause(self, i: int):
        self.workers[i].pause()

    def close(self, i: int):
        self.workers[i].close()

    def open(self, path, **args):
        # thread and worker.
        thread = MusicPlayerBackendThread()
        worker = MusicPlayerBackendWorker(path, **args)
        self.threads.append(thread)
        self.workers.append(worker)
        # move worker to thread.
        worker.moveToThread(thread)
        # thread slots.
        thread.started.connect(worker.init)
        thread.finished.connect(thread.deleteLater)
        # worker slots.
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        # start thread.
        thread.start()