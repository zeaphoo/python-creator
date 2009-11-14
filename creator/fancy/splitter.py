# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QRegion, QPainter
from theme import theme

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
        
        