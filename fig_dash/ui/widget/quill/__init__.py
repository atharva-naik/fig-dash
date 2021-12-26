#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union
# from pprint import pprint
# Qt5 imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize
from PyQt5.QtWidgets import QWidget, QApplication
# fig-dash imports.
from fig_dash.assets import FigD


class QuillEditor(QWebEngineView):
    '''Quill Editor instance loaded in a QWebEngineView. No external JS needed.'''
    def __init__(self, parent: Union[None, QWidget]=None, **kwargs):
        super(QuillEditor, self).__init__(parent)
        from fig_dash.ui.widget.quill.html import QuillHTML, QuillParams
        from fig_dash.ui.widget.quill.css import QuillSnowCSS, QuillEmojiCSS
        QuillHTML
        from fig_dash.ui.widget.quill.js import QuillJS, QuillEmojiJS
        from fig_dash.ui.widget.quill.css import QuillSnowCSS, QuillEmojiCSS
        from fig_dash.ui.widget.quill.html import QuillParams, QuillHTML

        QuillParams["JS"] = QuillJS
        QuillParams["SNOW_CSS"] = QuillSnowCSS
        QuillParams["EMOJI_JS"] = QuillEmojiJS
        QuillParams["EMOJI_CSS"] = QuillEmojiCSS
        QuillParams["EMOJI_IMAGE"] = kwargs.get('emojis', "")
        html = QuillHTML.render(QuillParams)

        self.setHtml(html)
        self.setZoomFactor(kwargs.get("zoom", 1.25))


def test_quill():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    quill = QuillEditor(emojis=FigD.icon("emojis.png"))
    quill.show()
    app.exec()


if __name__ == "__main__":
    test_quill()