# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import QPointF, QPoint
from theme import theme

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