#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import parse
import jinja2
import subprocess
from pathlib import Path
from typing import Union, Tuple
# Qt5 imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize, QObject, QThread
from PyQt5.QtWidgets import QWidget, QSizePolicy, QComboBox, QTextEdit, QToolButton, QToolBar, QVBoxLayout, QHBoxLayout, QApplication
# fig-dash imports.
from fig_dash.assets import FigD
setup_js = '''
function return_fn(a_string) { 
    return a_string; 
}
try {
    saveBtn = document.getElementById("save-notbook").getElementsByTagName("button")[0]
    saveBtn.style.display = "none"
    addCellBtn = insert_above_below.getElementsByTagName("button")[0]
    addCellBtn.style.display = "none"
    cutBtn = cut_copy_paste.getElementsByTagName("button")[0]
    copyBtn = cut_copy_paste.getElementsByTagName("button")[1]
    pasteBtn = cut_copy_paste.getElementsByTagName("button")[2]
    cutBtn.style.display = "none"
    copyBtn.style.display = "none"
    pasteBtn.style.display = "none"
    moveUpBtn = move_up_down.getElementsByTagName("button")[0]
    moveDownBtn = move_up_down.getElementsByTagName("button")[1]
    moveUpBtn.style.display = "none"
    moveDownBtn.style.display = "none" 
    runBtn = run_int.getElementsByTagName("button")[0]
    intBtn = run_int.getElementsByTagName("button")[1]
    restartBtn = run_int.getElementsByTagName("button")[2]
    restartAndRunBtn = run_int.getElementsByTagName("button")[3]
    runBtn.style.display = "none" 
    intBtn.style.display = "none" 
    restartBtn.style.display = "none" 
    restartAndRunBtn.style.display = "none"
    cmdBtn = cmd_palette.getElementsByTagName("button")[0]
    cmdBtn.style.display = "none"
    cell_type.style.display = "none"
    maintoolbar.style.display = "none"
    filelink.style.display = "none"
    editlink.style.display = "none"
    viewlink.style.display = "none"
    insertlink.style.display = "none"
    celllink.style.display = "none"
    kernellink.style.display = "none"
    widgetlink = document.getElementsByClassName("dropdown")[7].getElementsByTagName("a")[0] 
    helplink = document.getElementsByClassName("dropdown")[8].getElementsByTagName("a")[0]
    widgetlink.style.display = "none"
    helplink.style.display = "none"
    // hide the not trusted notification!
    notification_trusted.style.display = "none"
    kernel_name = document.getElementsByClassName("kernel_indicator_name")[0].textContent // kernel name/python version
    // kernel_indicator_icon // indicates if kernel is running or idle.
    // return a message.
    /* menubar_container = document.getElementById("menubar-container")
    menubar_container.style.display = "none";
    widget_menu = document.getElementById("widget-submenu")
    file_menu.style.display = ""
    edit_menu.style.display = ""
    view_menu.style.display = ""
    insert_menu.style.display = ""
    cell_menu.style.display = ""
    widget_menu.style.display = ""
    help_menu.style.display = "" */
    return_fn("Success");
}
catch(err) {
    console.error(err);
    return_fn("False");
}
'''
saveBtnClickJS = '''saveBtn.click()'''
addCellBtnClickJS = '''addCellBtn.click()'''
moveUpBtnClickJS = '''moveUpBtn.click()'''
moveDownBtnClickJS = '''moveDownBtn.click()'''
cutBtnClickJS = '''cutBtn.click()'''
copyBtnClickJS = '''copyBtn.click()'''
pasteBtnClickJS = '''pasteBtn.click()'''
runBtnClickJS = '''runBtn.click()'''
intBtnClickJS = '''intBtn.click()'''
restartBtnClickJS = '''restartBtn.click()'''
restartAndRunBtnClickJS = '''restartAndRunBtn.click()'''
cmdBtnClickJS = '''cmdBtn.click()'''
cellTypeChangeJS = lambda i: f'''
cell_type.selectedIndex = {i}
cell_type.dispatchEvent(new Event('change'));
'''
fileBtnClickJS = '''filelink.click()'''
editBtnClickJS = '''editlink.click()'''
viewBtnClickJS = '''viewlink.click()'''
insertBtnClickJS = '''insertlink.click()'''
cellBtnClickJS = '''celllink.click()'''
kernelBtnClickJS = '''kernellink.click()'''
widgetsBtnClickJS = '''widgetlink.click()'''
helpBtnClickJS = '''helplink.click()'''


notebook_btn_style = '''
QToolButton {
    border: 0px;
    background: transparent;
}
QToolButton:hover {
    background: #eb5f34;
}'''
jupyter_nb_widget_style = '''
QWidget {
    color: #fff;
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
}'''
class JupyterLoadWorker(QObject):
    finished = pyqtSignal(str, int)
    progress = pyqtSignal(str)

    def loadNB(self, **kwargs):
        name = kwargs.get("name")
        port = kwargs.get("port", "8888")
        '''launch jupyter notebook using subprocess'''
        args = [
            "jupyter-notebook", 
            f"--port={port}", 
            "--browser=n", "-y",
            "--NotebookApp.token=''",
            "--NotebookApp.password=''",
        ]
        if name is not None:
            path = str(Path(name).parent)
            args.append(f"--notebook-dir={path}")

        self.nb_process = subprocess.Popen(args, stderr=subprocess.PIPE)
        # self.nb_process = launch(**kwargs)
        nb_url = None
        while nb_url is None:
            line = self.nb_process.stderr.readline().decode("utf-8")
            # print(line)
            self.progress.emit(line)
            if "http://" in line:
                start = line.find("http://")
                end = line.find("/", start+len("http://"))
                nb_url = line[start:end]
        print(f"found notebook url: {nb_url}")
        name = kwargs.get("name")
        result = parse.parse("http://localhost:{}", nb_url) 
        actual_port = None
        if result is not None:
            actual_port = int(result[0])
        if name is not None:
            nb_url = f"http://localhost:{actual_port}/notebooks/{Path(name).name}"
            print(nb_url)
        self.finished.emit(nb_url, actual_port)

    def __del__(self):
        print("\x1b[31;1mdeleted JupyterLoadWorker\x1b[0m")


class CellTypeBox(QComboBox):
    def __init__(self, browser):
        super(CellTypeBox, self).__init__()
        self.browser = browser
        self.addItem("Code")
        self.addItem("Markdown")
        self.addItem("Raw NBConvert")
        self.addItem("Heading")
        self.currentIndexChanged.connect(self.changeCellType)
        self.setStyleSheet(jinja2.Template('''
            QComboBox {
                border: 0px;
                padding: 2px;
                color: #eb5f34;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
            }
            QComboBox::down-arrow {
                border: 0px;
                padding: 2px;
                background: transparent;
            }
            QComboBox::drop-down {
                border: 0px;
                padding: 2px;
                color: #eb5f34;
                image: url({{ IMAGE_URL }});
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
            }''').render(IMAGE_URL=FigD.icon("widget/jupyter_nb/down.svg")
        ))

    def changeCellType(self, i: int):
        self.browser.page().runJavaScript(
            cellTypeChangeJS(i)
        )


class NotebookBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, icon: str="", 
                 browser: Union[None, QWebEngineView]=None, 
                 js: str="", size: Tuple[int, int]=(20,20), tip="some tip"):
        super(NotebookBtn, self).__init__(parent)
        self.browser = browser
        self.js = js
        # set and size icon.
        icon = os.path.join("widget/jupyter_nb", icon)
        self.setIcon(FigD.Icon(icon))
        self.setIconSize(QSize(*size))
        # set tooltip for icon.
        self.setToolTip(tip)
        if browser: self.clicked.connect(self.callback)
        else: print("Notebook button is not connected to a browser instance.")
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }
        QToolButton:hover {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }''')
        
    def callback(self):
        # print(f"executing JS: {self.js}")
        self.browser.page().runJavaScript(self.js)


class JupyterLog(QTextEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(JupyterLog, self).__init__(parent)
        self.Log = []
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def append(self, text):
        self.Log.append(text)
        self.setText("\n".join(self.Log))


class CellToolbar(QWidget):
    def __init__(self, browser: Union[None, QWebEngineView]=None):
        super(CellToolbar, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.addCellBtn = NotebookBtn(
            self, icon="add_cell.png", 
            browser=browser, js=addCellBtnClickJS,
            tip="insert cell below"
        )
        self.moveUpBtn = NotebookBtn(
            self, icon="move_up.png", 
            browser=browser, js=moveUpBtnClickJS,
            tip="move selected cells up"
        )
        self.moveDownBtn = NotebookBtn(
            self, icon="move_down.png", 
            browser=browser, js=moveDownBtnClickJS,
            tip="move selected cells down"
        )
        self.cutBtn = NotebookBtn(
            self, icon="cut.png", 
            browser=browser, js=cutBtnClickJS,
            tip="cut selected cells"
        )
        self.copyBtn = NotebookBtn(
            self, icon="copy.png", 
            browser=browser, js=copyBtnClickJS,
            tip="copy selected cells"
        )
        self.pasteBtn = NotebookBtn(
            self, icon="paste.png", 
            browser=browser, js=pasteBtnClickJS,
            tip="paste cells below"
        )
        self.cellTypeBox = CellTypeBox(browser)
        # add all buttons.
        self.layout.addWidget(self.addCellBtn)
        self.layout.addWidget(self.moveUpBtn)
        self.layout.addWidget(self.moveDownBtn)
        self.layout.addWidget(self.cutBtn)
        self.layout.addWidget(self.copyBtn)
        self.layout.addWidget(self.pasteBtn)
        self.layout.addWidget(self.cellTypeBox)
        self.layout.addStretch(1)
        self.setObjectName("CellToolbar")
        self.setStyleSheet('''
        QWidget#CellToolbar {
            border: 0px;
            background: transparent;
        }''')
        self.setLayout(self.layout)    


class KernelToolbar(QWidget):
    def __init__(self, browser: Union[None, QWebEngineView]=None):
        super(KernelToolbar, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.runBtn = NotebookBtn(
            self, icon="run.svg", 
            browser=browser, js=runBtnClickJS,
            tip="run cell, select below"
        )
        self.intBtn = NotebookBtn(
            self, icon="interrupt.svg", 
            browser=browser, js=intBtnClickJS,
            tip="interrupt the kernel"
        )
        self.restartBtn = NotebookBtn(
            self, icon="restart.svg", 
            browser=browser, js=restartBtnClickJS,
            tip="restart the kernel (with dialog)"
        )
        self.restartAndRunBtn = NotebookBtn(
            self, icon="restart_and_run.svg", 
            browser=browser, js=restartAndRunBtnClickJS,
            tip="restart the kernel (with dialog)"
        )
        self.saveBtn = NotebookBtn(
            self, icon="save.png", 
            browser=browser, js=saveBtnClickJS,
            tip="Save and Checkpoint"
        )
        self.cmdBtn = NotebookBtn(
            self, icon="cmd_palette.png", 
            browser=browser, js=cmdBtnClickJS,
            tip="open the command palette"
        )
        self.layout.addWidget(self.runBtn)
        self.layout.addWidget(self.intBtn)
        self.layout.addWidget(self.restartBtn)
        self.layout.addWidget(self.restartAndRunBtn)
        self.layout.addWidget(self.saveBtn)
        self.layout.addWidget(self.cmdBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class JupyterMenuBar(QWidget):
    def __init__(self, browser: QWebEngineView):
        super(JupyterMenuBar, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.fileBtn = NotebookBtn(
            self, icon="file.png", 
            browser=browser, js=fileBtnClickJS,
            tip="toggle file menu"
        )
        self.editBtn = NotebookBtn(
            self, icon="edit.svg", 
            browser=browser, js=editBtnClickJS,
            tip="toggle edit menu"
        )
        self.viewBtn = NotebookBtn(
            self, icon="view.png", 
            browser=browser, js=viewBtnClickJS,
            tip="toggle view menu"
        )
        self.insertBtn = NotebookBtn(
            self, icon="insert.png", 
            browser=browser, js=insertBtnClickJS,
            tip="toggle insert menu"
        )
        self.cellBtn = NotebookBtn(
            self, icon="cell.png", 
            browser=browser, js=cellBtnClickJS,
            tip="toggle insert menu"
        )
        self.kernelBtn = NotebookBtn(
            self, icon="kernel.png", 
            browser=browser, js=kernelBtnClickJS,
            tip="toggle kernel menu"
        )
        self.widgetsBtn = NotebookBtn(
            self, icon="widgets.png", 
            browser=browser, js=widgetsBtnClickJS,
            tip="toggle widgets menu"
        )
        self.helpBtn = NotebookBtn(
            self, icon="help.png", 
            browser=browser, js=helpBtnClickJS,
            tip="toggle help menu"
        )
        self.layout.addWidget(self.fileBtn)
        self.layout.addWidget(self.editBtn)
        self.layout.addWidget(self.viewBtn)
        self.layout.addWidget(self.insertBtn)
        self.layout.addWidget(self.cellBtn)
        self.layout.addWidget(self.kernelBtn)
        self.layout.addWidget(self.widgetsBtn)
        self.layout.addWidget(self.helpBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class JupyterNavBar(QWidget):
    def __init__(self, browser: QWebEngineView):
        super(JupyterNavBar, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.backBtn = self.initBtn(text="back")
        self.nextBtn = self.initBtn(text="forward")
        self.reloadBtn = self.initBtn(text="reload")
        # connect callbacks.
        self.backBtn.clicked.connect(browser.back)
        self.nextBtn.clicked.connect(browser.forward)
        self.reloadBtn.clicked.connect(browser.reload)
        # add widgets.
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.nextBtn)
        self.layout.addWidget(self.reloadBtn)
        self.layout.addStretch(1)
        self.setStyleSheet('''
        QWidget {
            color: #eb5f34;
            border: 0px;
            background: transparent;
        }''')
        self.setLayout(self.layout)

    def initBtn(self, **kwargs):
        btn = QToolButton(self)
        btn.setText(kwargs.get("text", ""))
        icon = kwargs.get("icon")
        if icon is not None:
            btn.setIcon(FigD.Icon(icon))
        btn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            background: transparent;
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }''')
        # #eb5f34 (deep)
        # #f2e3df (light)
        # #db8b72 (dull)
        return btn


class SilentJSWebView(QWebEngineView):
    '''This doesn't work :('''
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        '''overried default behaviour of this function to silence console.error logging in PyQt5.'''
        pass


class JupyterNBWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: Union[str, None]=None, 
                 zoom_factor: float=1.25, port: int=8888):
        super(JupyterNBWidget, self).__init__(parent)
        self.zoom_factor = zoom_factor
        self.nb_process = None
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # browser setup.
        self.setupJS = setup_js
        self.browser = QWebEngineView()
        self.browser.setHtml("<h1 style='font-weight: bold;'>Loading Jupyter Notebook</h1>")
        self.browser.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        # log window.
        self.log_window = JupyterLog()
        self.log_window.setMaximumHeight(100)
        # navigation bar.
        self.navbar = JupyterNavBar(self.browser)
        # menu bar.
        self.menubar = JupyterMenuBar(self.browser)
        # cell editing/movement
        self.cellbar = CellToolbar(self.browser)
        # kernel control bar.
        self.kernelbar = KernelToolbar(self.browser)
        # kernel control tools.
        # self.kernelbar = KernelToolbar(self.browser)
        self.layout.addWidget(self.menubar)
        self.layout.addWidget(self.cellbar)
        self.layout.addWidget(self.kernelbar)
        self.layout.addWidget(self.navbar)
        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.log_window)
        # self.browser.loadFinished.connect(self.setupNB)
        self.browser.urlChanged.connect(self.monitorURL)
        # add widgets.
        # set layout.
        self.setLayout(self.layout)
        self.setStyleSheet(jupyter_nb_widget_style)
        # load jupyter notebook.
        # self.loadNB(port=port, name=name)

    def monitorURL(self):
        self.browser.setZoomFactor(self.zoom_factor)
        urlString = self.browser.url().toString()
        if urlString.endswith(".ipynb"):
            print(urlString)
            self.browser.loadFinished.connect(self.setupNB)

    def js_callback(self, msg: str):
        if msg != "Success":
            # print("\x1b[31;1mrescheduling JS\x1b[0m")
            self.browser.page().runJavaScript(self.setupJS, self.js_callback)

    def setupNB(self):
        self.browser.page().runJavaScript(self.setupJS, self.js_callback)

    def loadNB(self, **kwargs):
        '''load notebook using an external worker.'''
        import time
        s = time.time()
        self.nb_load_thread = QThread()
        self.nb_load_worker = JupyterLoadWorker()
        self.nb_load_worker.moveToThread(self.nb_load_thread)
        # after worker starts.
        # thread.
        self.nb_load_thread.started.connect(lambda: self.nb_load_worker.loadNB(**kwargs))
        self.nb_load_thread.finished.connect(self.nb_load_thread.deleteLater)
        # worker.
        self.nb_load_worker.finished.connect(self.loadNBUrl)
        self.nb_load_worker.finished.connect(self.nb_load_thread.quit)
        self.nb_load_worker.finished.connect(self.nb_load_worker.deleteLater)
        self.nb_load_worker.progress.connect(self.reportProgress)
        # start.
        self.nb_load_thread.start()
        print(f"started launcher worker in {time.time()-s}s")

    def loadNBUrl(self, url: str, port: int):
        print(f"\x1b[34;1mstarted notebook at port {port}\x1b[0m")
        self.browser.load(QUrl(url))

    def reportProgress(self, line: str):
        print(line)
        self.log_window.append(line)

    # def loadNB(self, **kwargs):
    #     self.nb_process = self.launch(**kwargs)
    #     nb_url = None
    #     while nb_url is None:
    #         line = self.nb_process.stderr.readline().decode("utf-8")
    #         print(line)
    #         self.log_window.append(line)
    #         if "http://" in line:
    #             start = line.find("http://")
    #             end = line.find("/", start+len("http://"))
    #             nb_url = line[start:end]
    #     print(f"found notebook url: {nb_url}")
    #     name = kwargs.get("name")
    #     result = parse.parse("http://localhost:{}", nb_url) 
    #     self.actual_port = None
    #     if result is not None:
    #         self.actual_port = int(result[0])
    #     if name is not None:
    #         nb_url = f"http://localhost:{self.actual_port}/notebooks/{Path(name).name}"
    #         print(nb_url)
    #     self.browser.load(QUrl(nb_url))
        # http://localhost:8932/notebooks/compute_stats.ipynb
    def launch(self, name: Union[str, None]=None, 
               port: int=8888, path: Union[str, None]=None):
        '''launch jupyter notebook using subprocess'''
        args = [
            "jupyter-notebook", 
            f"--port={port}", 
            "--browser=n", "-y",
            "--NotebookApp.token=''",
            "--NotebookApp.password=''",
        ]
        if name is not None:
            path = str(Path(name).parent)
            args.append(f"--notebook-dir={path}")
        # print(args)
        return subprocess.Popen(args, stderr=subprocess.PIPE)


def test_jupyter_nb(name: Union[str, None]=None):
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    # s = time.time()
    jupyter_nb = JupyterNBWidget(name=name)
    jupyter_nb.show()
    jupyter_nb.loadNB(port=5000, name=name)
    # print(time.time()-s)
    app.exec()


if __name__ == "__main__":
    # test_jupyter_nb(path="/home/atharva/Semester 6/BTP/YATS")
    test_jupyter_nb(name="/home/atharva/Semester 6/BTP/YATS/compute_stats.ipynb")