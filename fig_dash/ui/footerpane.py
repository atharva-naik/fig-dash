# footer pane contains shells, processes display, logs etc.


# # Qt5 imports.
# from PyQt5 import QtGui, QtCore, QtWidgets


# class WindowHighlightEffect(QtWidgets.QGraphicsEffect):
#     def __init__(self, offset=1.5, parent=None):
#         super(WindowHighlightEffect, self).__init__(parent)
#         self._color = QtGui.QColor(255, 255, 0, 128)
#         self._offset = offset * QtCore.QPointF(1, 1)

#     @property
#     def offset(self):
#         return self._offset

#     @property
#     def color(self):
#         return self._color

#     @color.setter
#     def color(self, color):
#         self._color = color

#     def boundingRectFor(self, sourceRect):
#         return sourceRect.adjusted(
#             -self.offset.x(), -self.offset.y(), self.offset.x(), self.offset.y()
#         )

#     def draw(self, painter):
#         offset = QtCore.QPoint()
#         try:
#             pixmap = self.sourcePixmap(QtCore.Qt.LogicalCoordinates, offset)
#         except TypeError:
#             pixmap, offset = self.sourcePixmap(QtCore.Qt.LogicalCoordinates)

#         bound = self.boundingRectFor(QtCore.QRectF(pixmap.rect()))
#         painter.save()
#         painter.setPen(QtCore.Qt.NoPen)
#         painter.setBrush(self.color)
#         p = QtCore.QPointF(offset.x() - self.offset.x(), offset.y() - self.offset.y())
#         bound.moveTopLeft(p)
#         painter.drawRoundedRect(bound, 5, 5, QtCore.Qt.RelativeSize)
#         painter.drawPixmap(offset, pixmap)
#         painter.restore()


# class BlurBackgroundEffect(QtWidgets.QGraphicsEffect):
#     def __init__(self, parent=None):
#         super(BlurBackgroundEffect, self).__init__(parent)
#         self._color = QtGui.QColor(255, 255, 0, 128)
#         # self._offset = offset * QtCore.QPointF(1, 1)

#     @property
#     def offset(self):
#         return self._offset

#     @property
#     def color(self):
#         return self._color

#     @color.setter
#     def color(self, color):
#         self._color = color

#     def boundingRectFor(self, sourceRect):
#         return sourceRect.adjusted(
#             -self.offset.x(), -self.offset.y(), self.offset.x(), self.offset.y()
#         )

#     def draw(self, painter):
#         offset = QtCore.QPoint()
#         try:
#             pixmap = self.sourcePixmap(QtCore.Qt.LogicalCoordinates, offset)
#         except TypeError:
#             pixmap, offset = self.sourcePixmap(QtCore.Qt.LogicalCoordinates)

#         bound = self.boundingRectFor(QtCore.QRectF(pixmap.rect()))
#         painter.save()
#         painter.setPen(QtCore.Qt.NoPen)
#         painter.setBrush(self.color)
#         p = QtCore.QPointF(offset.x() - self.offset.x(), offset.y() - self.offset.y())
#         bound.moveTopLeft(p)
#         painter.drawRoundedRect(bound, 5, 5, QtCore.Qt.RelativeSize)
#         painter.drawPixmap(offset, pixmap)
#         painter.restore()


# class BackgroundBlurEffect(QtWidgets.QGraphicsBlurEffect):
#     effectRect = None

#     def setEffectRect(self, rect):
#         self.effectRect = rect
#         self.update()

#     def draw(self, qp):
#         if self.effectRect is None or self.effectRect.isNull():
#             # no valid effect rect to be used, use the default implementation
#             super().draw(qp)
#         else:
#             qp.save()
#             # clip the drawing so that it's restricted to the effectRect
#             qp.setClipRect(self.effectRect)
#             # call the default implementation, which will draw the effect
#             super().draw(qp)
#             # get the full region that should be painted
#             fullRegion = QtGui.QRegion(qp.viewport())
#             # and subtract the effect rectangle
#             fullRegion -= QtGui.QRegion(self.effectRect)
#             qp.setClipRegion(fullRegion)
#             # draw the *source*, which has no effect applied
#             self.drawSource(qp)
#             qp.restore()
# import os
# from typing import Union, Tuple
# from PyQt5.QtGui import QColor, QKeySequence
# from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize, QPoint
# from PyQt5.QtWidgets import QMenu, QLabel, QWidget, QAction, QMainWindow, QApplication, QVBoxLayout, QGraphicsBlurEffect
# # fig dash imports.
# from fig_dash.assets import FigD


# class BlurLabel(QWidget):
#     def __init__(self, parent: Union[None, QWidget]=None, text: str=""):
#         super(BlurLabel, self).__init__(parent)
#         # self.setAttribute(Qt.WA_StyledBackground)
#         self.widget = QWidget()
#         effect = QGraphicsBlurEffect(blurRadius=10)
#         self.widget.setGraphicsEffect(effect)
#         self._label = QLabel(text)
#         self.layout = QVBoxLayout(self)
#         self.layout.setContentsMargins(0,0,0,0)
#         self.layout.addWidget(self.widget)
#         self.label.setParent(self)
#         self.move(self.width()//2, self.height()//2)
#         self.setAttribute(Qt.WA_TranslucentBackground)

#     @property
#     def label(self):
#         return self._label

#     def sizeHint(self):
#         return self._label.sizeHint()

#     def resizeEvent(self, event):
#         self._label.resize(self.size())
#         self._label.raise_()
#         self.move(self.width()//2, self.height()//2)
#         return super().resizeEvent(event)

#     def setStyleSheet(self, stylesheet):
#         self.widget.setStyleSheet(stylesheet)


# class BlurMenu(QWidget):
#     def __init__(self, parent: Union[None, QWidget]):
#         super(BlurMenu, self).__init__(parent)
#         self.widget = QWidget()
#         blur_effect = QGraphicsBlurEffect(blurRadius=5)
#         self.widget.setGraphicsEffect(blur_effect)

#         self._menu = QMenu(parent=self)
#         self.menu.setStyleSheet(""" background-color : transparent; color : black""")
#         self.menu.setContentsMargins(0, 0, 0, 0)

#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(self.widget)
#         self.setLayout(self.layout)

#     @property
#     def menu(self):
#         return self._menu

#     def sizeHint(self):
#         return self._menu.sizeHint()

#     def resizeEvent(self, event):
#         self._menu.resize(self.size())
#         self._menu.raise_()
#         return super().resizeEvent(event)


# class TestWindow(QMainWindow):
#     def contextMenuEvent(self, event):
#         self.menu = BlurMenu(self)
#         self.menu.widget.setStyleSheet("""
#         QWidget { 
#             background: rgba(0,0,0,0.9); 
#             color: #fff;
#         }""")
#         self.menu.addAction(QAction("Test 1"))
#         self.menu.addAction(QAction("Test 2"))
#         print("context menu event")
#         self.menu.menu.popup(event.globalPos())


# def test_blurmenu():
#     import sys
#     FigD("/home/atharva/GUI/fig-dash/resources")
#     app = QApplication(sys.argv)
#     window = TestWindow()
#     window.show()
#     app.exec()

# def test_blurlabel():
#     import sys
#     FigD("/home/atharva/GUI/fig-dash/resources")
#     app = QApplication(sys.argv)
#     label = BlurLabel(text="For the record, I think the widget does have a transparent background, but it's obviously sitting on something else that doesn't")
#     label.setStyleSheet("background: rgba(29,29,29,0.9); color: #fff;")
#     label.show()
#     app.exec()


# if __name__ == "__main__":
#     # test_blurmenu()
#     test_blurlabel()