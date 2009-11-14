# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import QRect
from theme import theme

class StyledBar(QWidget):
    def __init__(self, parent = None):
        super(StyledBar, self).__init__(parent)
        self._singleRow = True
        self._topBorder = False
        self.setFixedHeight(theme.navigationWidgetHeight)
        
    def setSingleRow(self, single):
        self._singleRow = single
    
    def isSingleRow(self):
        return self._singleRow
    
    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOption()
        option.rect = self.rect()
        option.state = QStyle.State_Horizontal
        self._drawStyledBar(painter, option)
        
    def _drawStyledBar(self, painter, option):
        rect = option.rect
        key = "fancy styledbar %d %d %d" %(rect.width(), rect.height(), theme.baseColor.rgb())
        pixmap = QPixmap()
        p = painter
        if  theme.usePixmapCache() and not QPixmapCache.find(key, pixmap):
            pixmap = QPixmap(rect.size())
            p = QPainter(pixmap)
            rect = QRect(0, 0, rect.width(), rect.height())

        horizontal = option.state & QStyle.State_Horizontal
        offset = self.window().mapToGlobal(option.rect.topLeft()) - self.mapToGlobal(option.rect.topLeft())
        gradientSpan = QRect(offset, self.window().size())
        
        if horizontal:
            theme.horizontalGradient(p, gradientSpan, rect)
        else:
            theme.verticalGradient(p, gradientSpan, rect)

        painter.setPen(theme.borderColor)

        if horizontal:
            lighter = QColor(255, 255, 255, 40)
            if self._topBorder:
                p.drawLine(rect.topLeft(), rect.topRight())
                p.setPen(lighter)
                p.drawLine(rect.topLeft() + QPoint(0, 1), rect.topRight() + QPoint(0, 1))
            else:
                p.drawLine(rect.bottomLeft(), rect.bottomRight())
                p.setPen(lighter)
                p.drawLine(rect.topLeft(), rect.topRight())
        else:
            p.drawLine(rect.topLeft(), rect.bottomLeft())
            p.drawLine(rect.topRight(), rect.bottomRight())
            
        if theme.usePixmapCache() and not QPixmapCache.find(key, pixmap):
            painter.drawPixmap(rect.topLeft(), pixmap)
            p.end()
            del p
            QPixmapCache.insert(key, pixmap)
        
class StyledSeparator(QWidget):
    def __init__(self, parent = None):
        super(StyledSeparator, self).__init__(parent)
        self.setFixedWidth(10)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOption()
        option.rect = self.rect()
        option.state = QStyle.State_Horizontal
        option.palette = self.palette()
        self._drawStyledSeparator(painter, option)
    
    def _drawStyledSeparator(self, painter, option):
        separatorColor = theme.borderColor
        separatorColor.setAlpha(100)
        painter.setPen(separatorColor)
        margin = 6
        rect = option.rect
        if option.state & State_Horizontal:
            offset = rect.width()/2
            painter.drawLine(rect.bottomLeft().x() + offset,
                        rect.bottomLeft().y() - margin,
                        rect.topLeft().x() + offset,
                        rect.topLeft().y() + margin)
        else:
            offset = rect.height()/2
            painter.setPen(QPen(option.palette.background().color().darker(110)))
            painter.drawLine(rect.topLeft().x() + margin ,
                        rect.topLeft().y() + offset,
                        rect.topRight().x() - margin,
                        rect.topRight().y() + offset)
