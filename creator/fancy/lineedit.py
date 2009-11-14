# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PanelLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super(PanelLineEditor, self).__init__(parent)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        panel = QStyleOptionFrameV2()
        self.initStyleOption(panel)
        