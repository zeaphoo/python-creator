# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from fancystyle import fancystyle

class ToolButton(QToolButton):
    def __init__(self, parent=None):
        super(ToolButton, self).__init__(parent)
        
    def paintEvent(self, event):
        p = QStylePainter(self)
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        fancystyle.draw_ToolButton(opt, p, self)

class OutputToggleButton(QPushButton):
    def __init__(self, number, text, parent = None):
        super(OutputToggleButton, self).__init__(parent)
        self._number = number
        self._text = text
        self.setFocusPolicy(Qt.NoFocus)
        self.setCheckable(True)
        self.setStyleSheet(
            "QPushButton { border-image: url(:/fancy/images/panel_button.png) 2 2 2 19;"
                         " border-width: 2px 2px 2px 19px; padding-left: -17; padding-right: 4 } "
            "QPushButton:checked { border-image: url(:/fancy/images/panel_button_checked.png) 2 2 2 19 } "
            "QPushButton:checked:hover { border-image: url(:/fancy/images/panel_button_checked_hover.png) 2 2 2 19 } "
            "QPushButton:pressed:hover { border-image: url(:/fancy/images/panel_button_pressed.png) 2 2 2 19 } "
            "QPushButton:hover { border-image: url(:/fancy/images/panel_button_hover.png) 2 2 2 19 } "
            )
    
    def sizeHint(self):
        self.ensurePolished()
        s = self.fontMetrics().size(Qt.TextSingleLine, self._text)
        #Expand to account for border image set by stylesheet above
        s.rwidth += (19 + 5 + 2)
        s.rheight += (2 + 2)
        return s.expandedTo(QApplication.globalStrut())
        
    def paintEvent(self, event):
        QPushButton.paintEvent(event)
        fm = self.fontMetrics()
        baseLine = (self.height() - fm.height() + 1) / 2 + fm.ascent()
        numberWidth = fm.width(self._number)
        
        p = QPainter(self)
        p.setFont(font())
        p.setPen(Qt.white)
        p.drawText((20 - numberWidth) / 2, baseLine, self._number)
        if not isChecked():
            p.setPen(Qt.black)
        leftPart = 22
        p.drawText(leftPart, baseLine, fm.elidedText(self._text, Qt.ElideRight, 
                                                     self.width() - leftPart - 1))
        
    