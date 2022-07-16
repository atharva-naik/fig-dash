#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import webbrowser
from typing import *
from functools import partial
from PyQt5.QtCore import QObject, QThread, pyqtSignal

# Worker for searching using google image search
class GoogleImageSearchWorker(QObject):
    finished = pyqtSignal()
    urlFetched = pyqtSignal(str)
    def __init__(self):
        super(GoogleImageSearchWorker, self).__init__()
        self.searchUrl = 'http://www.google.com/searchbyimage/upload'

    def fromUrl(self, url: str) -> str:
        import requests
        multipart = {
            'encoded_image': (
                url, open(url, 'rb')
            ), 
            'image_content': ''
        }
        response = requests.post(
            self.searchUrl, files=multipart, 
            allow_redirects=False
        )
        fetchUrl = response.headers.get('Location', "NOT_FOUND")
        self.urlFetched.emit(fetchUrl)
        self.finished.emit()

        return fetchUrl        

    def fromLocalFile(self, filePath: str):
        """Returns google image search url for a local file.
        Args:
            filePath (str): _description_
        """
        import requests
        multipart = {
            'encoded_image': (
                filePath, 
                open(filePath, 'rb')
            ), 
            'image_content': ''
        }
        response = requests.post(
            self.searchUrl, files=multipart, 
            allow_redirects=False
        )
        fetchUrl = response.headers.get('Location', "NOT_FOUND")
        self.urlFetched.emit(fetchUrl)
        self.finished.emit()

# google image searching backend.
class GoogleImageSearchBackend(QObject):
    urlFetched = pyqtSignal(str)
    def __init__(self):
        super(GoogleImageSearchBackend, self).__init__()
        self.threads = []
        self.workers = []

    def start(self, path: Union[str, None]=None, url: Union[str, None]=None):
        # thread and worker.
        thread = QThread()
        worker = GoogleImageSearchWorker()
        self.threads.append(thread)
        self.workers.append(worker)
        # move worker to thread.
        worker.moveToThread(thread)
        # thread slots.
        if path is not None:
            func = partial(worker.fromLocalFile, path)
        elif url is not None:
            func = partial(worker.fromUrl, url) 
        thread.started.connect(func)
        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.urlFetched.connect(self.emitUrl)
        # start thread.
        thread.start()

    def emitUrl(self, url: str):
        self.urlFetched.emit(url)