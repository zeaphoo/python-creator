# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from fancystyle import fancystyle
from theme import theme

class ToolButton(QToolButton):
    def __init__(self, parent=None):
        super(ToolButton, self).__init__(parent)
        
    def paintEvent(self, event):
        p = QStylePainter(self)
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        fancystyle.draw_ToolButton(opt, p, self)

class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent)
    
    def paintEvent(self, event):
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.Text))
    
        #draw the combobox frame, focusrect and selected etc.
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        fancystyle.draw_ComboBox(opt, painter, self)
        
        #draw the icon and text
        fancystyle.draw_ComboBoxLabel(opt, painter, self)


class PanelLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super(PanelLineEditor, self).__init__(parent)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        panel = QStyleOptionFrameV2()
        self.initStyleOption(panel)
        

class Splitter(QtGui.QSplitter):    
    def __init__(self, orientation=None, parent=None):
        super(Splitter, self).__init__(parent)
        if orientation and orientation.lower() == 'horizontal':
            ort = Qt.Horizontal
        else:
            ort = Qt.Vertical 
        self.setHandleWidth(1)
        self.setChildrenCollapsible(False)
        
    def createHandle(self):
        return SplitterHandle(self.orientation(), self)
    
    
class SplitterHandle(QtGui.QSplitterHandle):
    def __init__(self, orientation, splitter):
        super(SplitterHandle, self).__init__(orientation, splitter)
        self.setMask(QRegion(self.contentsRect()))
        self.setAttribute(Qt.WA_MouseNoMask, True)
        
    def resizeEvent(self, event):
        if self.orientation() == Qt.Horizontal:
            self.setContentsMargins(2, 0, 2, 0)
        else:
            self.setContentsMargins(0, 2, 0, 2)
        self.setMask(QRegion(self.contentsRect()))
        QtGui.QSplitterHandle.resizeEvent(self, event)
        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), theme.borderColor)
        

class StatusBar(QStatusBar):
    def __init__(self, parent = None):
        super(StatusBar, self).__init__(parent)
        self.setFixedHeight(theme.navigationWidgetHeight + 2)
    
    def paintEvent(self, event):
        p = QPainter(self)
        opt = QStyleOption()
        opt.initFrom(self)
        self.drawPanelStatusBar(p, opt)
        
    def drawPanelStatusBar(self, painter, option):
        rect = option.rect
        painter.save()
        grad = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.center().x(), rect.bottom()))
        startColor = theme.shadowColor.darker(164)
        endColor = theme.baseColor.darker(130)
        grad.setColorAt(0, startColor)
        grad.setColorAt(1, endColor)
        painter.fillRect(option.rect, grad)
        painter.setPen(QColor(255, 255, 255, 60))
        painter.drawLine(rect.topLeft() + QPoint(0,1),
                          rect.topRight()+ QPoint(0,1))
        painter.setPen(theme.borderColor.darker(110))
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.restore()
