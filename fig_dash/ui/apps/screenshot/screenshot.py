#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
import pyautogui
from PIL.ImageQt import ImageQt
# Qt5 imports.
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence, QPalette, QBrush
from PyQt5.QtCore import Qt, QEvent, QT_VERSION_STR, QSize, QRect, QPoint
from PyQt5.QtWidgets import QSplitter, QApplication, QMainWindow, QWidget, QTabBar, QVBoxLayout, QHBoxLayout, QToolButton, QSizePolicy, QSpacerItem, QShortcut, QFileDialog, QRubberBand, QGraphicsDropShadowEffect
# fig-dash imports.
from fig_dash.utils import *
from fig_dash.assets import FigD
from fig_dash.ui.widget.boolean_toggle import BooleanToggleBtn


class ScreenShotSelection(QWidget):
    """overlay this widget on the entire screen to allow for selections"""
    def __init__(self, app):
        super(ScreenShotSelection, self).__init__()
        screen_rect = app.desktop().screenGeometry()
        width, height = screen_rect.width(), screen_rect.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setCursor(Qt.CrossCursor)
        self.setWindowOpacity(0.5)
        self.ui = None

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(QRect(
            self.origin, QSize()
        ))
        self.rubberband.show()
        super(ScreenShotSelection, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(QRect(
                self.origin, 
                event.pos()
            ).normalized())
        super(ScreenShotSelection, self).mouseMoveEvent(event)

    def connectScreenshotUI(self, ui):
        self.ui = ui
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)

    def mouseReleaseEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            rect = self.rubberband.geometry()
            if self.ui: 
                # x = rect.x()
                # y = rect.y()
                # w = rect.width()
                # h = rect.height()
                # x1 = x
                # y1 = y
                # x2 = x + w
                # y2 = y + h
                # region = (x1, y1, x2, y2)
                self.hide()
                pyqtSleep(200)
                # img = pyautogui.screenshot(region=region)
                screen = QApplication.instance().primaryScreen()
                desktop = QApplication.instance().desktop()
                imgmap = screen.grabWindow(
                    desktop.winId(), rect.x()+80, rect.y()+25, 
                    rect.width(), rect.height()
                )
                # print(imgmap)
            self.ui.savePixmap(imgmap)
        super(ScreenShotSelection, self).mouseReleaseEvent(event)


class DelayBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None) -> None:
        super(DelayBtn, self).__init__(parent)
        self.setText("0s")
        self.setIcon(FigD.Icon("apps/screenshot/delay.svg"))
        self.setIconSize(QSize(30,30))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 16px;
            border-radius: 10px;
            background: transparent;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 100);
        }""")


class RecordingScopeSelector(QWidget):
    '''
    widget container for buttons to select scope of recording:
    1) geometric (square) selection
    2) screen
    3) window
    '''
    def __init__(self) -> None:
        super(RecordingScopeSelector, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # create buttons.
        self.freeSelectBtn = self.initScopeBtn(
            icon="free_selection.svg", text="Free Form",
            tip="select free form area for screenshot"
        )
        self.selectBtn = self.initScopeBtn(
            icon="select.svg", text="Select",
            tip="select rectangle on screen for capture"
        )
        self.screenBtn = self.initScopeBtn(
            icon="screen.svg", text="Screen",
            tip="capture the whole screen"
        )
        self.windowBtn = self.initScopeBtn(
            icon="window.svg", text="Window",
            tip="Capture a particular window"
        )
        self.scrollBtn = self.initScopeBtn(
            icon="scroll.svg", text="Scroll",
            tip="Capture a scrolling screenshot"
        )
        # setup shit.
        self.btn_list = [
            self.freeSelectBtn,
            self.selectBtn,
            self.screenBtn,
            self.windowBtn,
            self.scrollBtn,
        ]
        self.ui = None
        self.state_index = 1
        self.setIndex(1)
        # connect to slots.
        self.freeSelectBtn.clicked.connect(self.freeSelect)
        self.selectBtn.clicked.connect(self.select)
        self.screenBtn.clicked.connect(self.screen)
        self.windowBtn.clicked.connect(self.window)
        self.scrollBtn.clicked.connect(self.scroll)
        # build layout.
        self.layout.addWidget(self.freeSelectBtn)
        self.layout.addWidget(self.selectBtn)
        self.layout.addWidget(self.screenBtn)
        self.layout.addWidget(self.windowBtn)
        self.layout.addWidget(self.scrollBtn)
        self.setLayout(self.layout)

    def setIndex(self, i: int):
        j = self.index() 
        self.btn_list[j].setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 16px;
            border-radius: 10px;
            background: transparent;
        }""")
        self.state_index = i
        self.btn_list[i].setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 16px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 100);
        }""")

    def index(self) -> int:
        return self.state_index

    def connectScreenshotUI(self, ui):
        self.ui = ui

    def freeSelect(self):
        """set recording mode to select rectangle"""
        self.setIndex(0)

    def select(self):
        """set recording mode to select rectangle"""
        self.setIndex(1)

    def screen(self):
        """set recording mode to whole screen"""
        self.setIndex(2)

    def window(self):
        """set recording mode to a window"""
        self.setIndex(3)

    def scroll(self):
        """set recording mode to scrolling screenshot"""
        self.setIndex(4)

    def initScopeBtn(self, **args):
        btn = QToolButton()
        icon = args.get("icon")
        if icon:
            icon = FigD.Icon(os.path.join(
                "apps/screenshot",
                icon
            ))
        btn.setIcon(icon)
        btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 16px;
            border-radius: 10px;
            background: transparent;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 100);
        }""")
        btn.setIconSize(QSize(35,35))
        btn.setText(args.get("text","text"))
        btn.setToolTip(args.get("tip", "a tip"))
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        return btn


class MoreOptions(QWidget):
    """
    filters, border/outline, settings.
    """
    def __init__(self) -> None:
        super(MoreOptions, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # create buttons.
        self.filtersBtn = self.initMoreBtn(
            icon="filters.svg", text="Filters",
            tip="apply filters on video/screenshot"
        )
        # make this a dropdown.
        self.borderBtn = self.initMoreBtn(
            icon="border.svg", text="Border",
            tip="add an outline to screenshot"
        )
        self.settingsBtn = self.initMoreBtn(
            icon="settings.svg", text="Settings",
            tip="open screenshot settings."
        )
        # connect to slots.
        self.borderBtn.clicked.connect(self.border)
        self.filtersBtn.clicked.connect(self.filters)
        self.settingsBtn.clicked.connect(self.settings)
        # build layout.
        self.layout.addWidget(self.borderBtn)
        self.layout.addWidget(self.filtersBtn)
        self.layout.addWidget(self.settingsBtn)
        self.setLayout(self.layout)

    def border(self):
        pass

    def filters(self):
        pass

    def settings(self):
        pass

    def initMoreBtn(self, **args):
        btn = QToolButton()
        icon = args.get("icon")
        if icon:
            icon = FigD.Icon(os.path.join(
                "apps/screenshot",
                icon
            ))
        btn.setIcon(icon)
        btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 14px;
            border-radius: 10px;
            background: transparent;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 100);
        }""")
        btn.setIconSize(QSize(25,25))
        btn.setText(args.get("text","text"))
        btn.setToolTip(args.get("tip", "a tip"))
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        return btn


class ScreenshotSaveModeSelector(QWidget):
    """
    select the saving mode for the screenshot.
    """
    def __init__(self) -> None:
        super(ScreenshotSaveModeSelector, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # create buttons.
        self.shareBtn = self.initScopeBtn(
            icon="share.svg", text="Share",
            tip="share image."
        )
        self.editBtn = self.initScopeBtn(
            icon="edit.svg", text="Edit",
            tip="open image in editor."
        )
        self.copyBtn = self.initScopeBtn(
            icon="copy_to_clipboard.svg", text="Clipboard",
            tip="copy screenshot to clipboard."
        )
        self.saveBtn = self.initScopeBtn(
            icon="save.svg", text="Save",
            tip="save screenshot image locally."
        )
        # self.fileDropdown
        # setup shit.
        self.btn_list = [
            self.copyBtn,
            self.saveBtn,
            self.editBtn,
            self.shareBtn,
        ]
        self.state_index = 1
        self.setIndex(1)
        # connect to slots.
        self.copyBtn.clicked.connect(self.copyMode)
        self.saveBtn.clicked.connect(self.saveMode)
        self.editBtn.clicked.connect(self.editMode)
        self.shareBtn.clicked.connect(self.shareMode)
        # build layout.
        self.layout.addWidget(self.copyBtn)
        self.layout.addWidget(self.saveBtn)
        self.layout.addWidget(self.editBtn)
        self.layout.addWidget(self.shareBtn)
        self.setLayout(self.layout)

    def setIndex(self, i: int):
        j = self.index() 
        self.btn_list[j].setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 14px;
            border-radius: 10px;
            background: transparent;
        }""")
        self.state_index = i
        self.btn_list[i].setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 14px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 100);
        }""")

    def index(self) -> int:
        return self.state_index

    def copyMode(self):
        """set recording mode to select rectangle"""
        self.setIndex(0)

    def saveMode(self):
        """set recording mode to whole screen"""
        self.setIndex(1)

    def editMode(self):
        """open screenshot in editor"""
        self.setIndex(2)

    def shareMode(self):
        """open screenshot in share mode"""
        self.setIndex(3)

    def initScopeBtn(self, **args):
        btn = QToolButton()
        icon = args.get("icon")
        if icon:
            icon = FigD.Icon(os.path.join(
                "apps/screenshot",
                icon
            ))
        btn.setIcon(icon)
        btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 14px;
            border-radius: 10px;
            background: transparent;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 100);
        }""")
        btn.setIconSize(QSize(30,30))
        btn.setText(args.get("text","text"))
        btn.setToolTip(args.get("tip", "a tip"))
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        return btn

# screen-shot UI
class DashScreenshotUI(QMainWindow):
    def __init__(self, app: Union[None, QApplication]=None):
        super(DashScreenshotUI, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        centralWidget = self.initCentralWidget()
        self.setCentralWidget(centralWidget)
        self.setWindowOpacity(0.98)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.app = app
        self.scopeSelector.connectScreenshotUI(self)
        # ESC key to close screenshot UI.
        self.Esc = QShortcut(Qt.Key_Escape, self)
        self.Esc.activated.connect(self.close)
        # Enter key to take screenshot.
        self.Enter = QShortcut(Qt.Key_Return, self)
        self.Enter.activated.connect(self.takeScreenshot)
        self.recordBtn.clicked.connect(
            self.takeScreenshot
        )
        self.screen_shot_selection = ScreenShotSelection(self.app)
        self.screen_shot_selection.connectScreenshotUI(self)
        # add shadow effect.
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(500)
        shadow_effect.setOffset(0,0)
        self.setGraphicsEffect(shadow_effect)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        super(DashScreenshotUI, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except Exception as e:
            print("\x1b[31;1mui.apps.screenshot.DashScreenShotUI.mouseMoveEvent\x1b[0m", e)

    def savePixmap(self, pixmap):
        # handle save mode.
        if self.saveModeSelector.index() == 1:
            pictures = os.path.expanduser("~/Pictures")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            default_path = os.path.join(pictures, f"Screenshot from {timestamp}.png")
            path, _ = QFileDialog.getSaveFileName(
                self, "Save Screenshot as", 
                default_path, 'Images (*.png)'
            )
            # print("path:", path)
            if path != "": 
                print(f"\x1b[32;1m saved to path: {path} \x1b[0m")
                pixmap.save(path)
            self.close()
        # handle copy to clipboard mode.
        else:
            self.pixmap = pixmap
            if self.app is not None:
                self.app.clipboard().setPixmap(self.pixmap)
                print("copied image to clipboard.")
            self.show()

    def saveScreenshot(self, img):
        # handle save mode.
        if self.saveModeSelector.index() == 1:
            pictures = os.path.expanduser("~/Pictures")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            default_path = os.path.join(pictures, f"Screenshot from {timestamp}.png")
            path, _ = QFileDialog.getSaveFileName(
                self, "Save Screenshot as", 
                default_path, 'Images (*.png)'
            )
            # print("path:", path)
            if path != "": 
                print(f"\x1b[32;1m saved to path: {path} \x1b[0m")
                img.save(path)
            self.close()
        # handle copy to clipboard mode.
        else:
            self.qim = ImageQt(img)
            self.pixmap = QPixmap.fromImage(self.qim)
            if self.app is not None:
                self.app.clipboard().setPixmap(self.pixmap)
                print("copied image to clipboard.")
            self.show()

    def takeScreenshot(self):
        """take screenshot."""
        # hide screenshot UI.
        self.hide()
        pyqtSleep(200)
        # entire screen.
        if self.scopeSelector.index() == 1:
            self.screen_shot_selection.show()
            return
            # img = pyautogui.screenshot(region=(0, 0, 300, 400))
        elif self.scopeSelector.index() == 2:
            img = pyautogui.screenshot()
        elif self.scopeSelector.index() == 4:
            img_list = []
            for i in range(5):
                pyautogui.scroll(10)
                pyqtSleep(200)
                img_list.append(pyautogui.screenshot())
            print(img_list)
        self.saveScreenshot(img)

    def initCentralWidget(self):
        centralWidget = QWidget()
        centralWidget.setStyleSheet("""
        QWidget {
            border-radius: 20px;
            /* background: #292929; */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }""")
        # delay button.
        self.delayBtn = DelayBtn()
        self.videoToggle = DelayBtn()
        delayBtn = self.delayBtn
        videoToggle = BooleanToggleBtn()
        # record button.
        recordBtn = self.initRecordBtn()
        self.recordBtn = recordBtn
        # recording scope selector.
        scopeSelector = RecordingScopeSelector()
        self.scopeSelector = scopeSelector
        # save mode selector.
        saveModeSelector = ScreenshotSaveModeSelector()
        self.saveModeSelector = saveModeSelector
        # record widget.
        recordWidget = QWidget()
        recordWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        recordLayout = QHBoxLayout()
        recordWidget.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            background: transparent;
        }""")
        recordLayout.setContentsMargins(0, 0, 0, 0)
        recordLayout.setSpacing(80)
        recordLayout.addWidget(videoToggle, 0, Qt.AlignVCenter)
        recordLayout.addStretch(1)
        recordLayout.addWidget(recordBtn, 0, Qt.AlignVCenter)
        recordLayout.addStretch(1)
        recordLayout.addWidget(delayBtn, 0, Qt.AlignVCenter)
        recordWidget.setLayout(recordLayout)
        # more options widget.
        self.moreOptionsSelector = MoreOptions()
        moreOptionsSelector = self.moreOptionsSelector
        # build layout.
        layout = QVBoxLayout()
        layout.addWidget(scopeSelector)
        layout.addWidget(saveModeSelector)
        layout.addWidget(moreOptionsSelector)
        layout.addWidget(recordWidget, 0, Qt.AlignCenter)
        centralWidget.setLayout(layout)
        centralWidget.recordBtn = recordBtn

        return centralWidget

    def initRecordBtn(self):
        btn = QToolButton()
        btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            padding: 5px;
            font-size: 16px;
            border-radius: 34px;
            background: transparent;
        }
        QToolButton:hover {
            background: rgba(255, 255, 255, 100);
        }""")
        btn.setIconSize(QSize(55,55))
        btn.setIcon(FigD.Icon(os.path.join(
            "apps/screenshot",
            "record.svg"
        )))
        btn.setToolTip("Take the screenshot/start recording screen")
        
        return btn

def test_screenshot_ui():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    w, h = screen_rect.width()//2, screen_rect.height()//2
    screenshot_ui = DashScreenshotUI(app=app)
    screenshot_ui.move(w, h)
    screenshot_ui.show()
    app.exec()


if __name__ == "__main__":
    test_screenshot_ui()
    # memory = io.BytesIO()
    # img.save(memory, format="png")
    # klembord.set({"image/png": memory.getvalue()})
    # print("copied image to clipboard")