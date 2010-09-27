# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QPainter, QColor

class EdgeLine(QWidget):
    def __init__(self, editor):
        super(EdgeLine, self).__init__(editor)
        self.code_editor = editor
        self.column = 80
        
    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor(Qt.darkGray)
        color.setAlphaF(.5)
        painter.fillRect(event.rect(), color)
