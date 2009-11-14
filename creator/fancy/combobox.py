# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from fancystyle import fancystyle

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
