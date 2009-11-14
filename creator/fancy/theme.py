# -*- coding: utf-8 -*-

from PyQt4.QtGui import QColor, QPixmap, QPixmapCache, QPainter, QLinearGradient
from PyQt4.QtCore import Qt, QRect, QPoint, QPointF

def clamp(x):
    val = 255 if x > 255 else int(x)
    return 0 if val < 0 else val
    
class Theme():
    navigationWidgetHeight = 24
    buttonTextColor = QColor(0x4c4c4c)
    def __init__(self):
        self._baseColor = QColor(0x666666)
        self._usePixmapCache = True
        self._initTheme()
    
    def getBaseColor(self):
        return self._baseColor
    
    def setBaseColor(self, color):
        self_baseColor = color
        self._initTheme()
        
    baseColor = property(getBaseColor, setBaseColor)
    
    def getPanelTextColor(self):
        return Qt.white
        
    panelTextColor = property(getPanelTextColor)
    
    def usePixmapCache(self):
        return self._usePixmapCache
        
    def getSidebarFontSize(self):
        return 7.5
    
    sidebarFontSize = property(getSidebarFontSize)
    
    def verticalGradient(self, painter, spanRect, clipRect):
        key = 'fancy vertical gradient %d %d %d %d %d'%(spanRect.width(), spanRect.height(), clipRect.width(),
                                             clipRect.height(), self.baseColor.rgb())
        pixmap = QPixmap()
        p = painter
        rect = QRect(clipRect)
        
        if self._usePixmapCache and not QPixmapCache.find(key, pixmap):
            pixmap = QPixmap(clipRect.size())
            p = QPainter(pixmap)
            rect = QRect(0, 0, clipRect.width(), clipRect.height())
        
        base = self.baseColor
        grad = QLinearGradient(QPointF(spanRect.topRight()), QPointF(spanRect.topLeft()))
        grad.setColorAt(0, self.highlightColor)
        grad.setColorAt(0.301, base)
        grad.setColorAt(1, self.shadowColor)
        p.fillRect(rect, grad)
        
        light = QColor(255, 255, 255, 80)
        p.setPen(light)
        p.drawLine(rect.topRight() - QPoint(1, 0), rect.bottomRight() - QPoint(1, 0))
        
        if self._usePixmapCache and not QPixmapCache.find(key, pixmap):
            painter.drawPixmap(clipRect.topLeft(), pixmap)
            p.end()
            del p
            QPixmapCache.insert(key, pixmap)
    
    def horizontalGradient(self, painter, spanRect, clipRect):
        key = 'fancy vertical gradient %d %d %d %d %d'%(spanRect.width(), spanRect.height(), clipRect.width(),
                                             clipRect.height(), self.baseColor.rgb())
        pixmap = QPixmap()
        p = painter
        rect = QRect(clipRect)
        
        if self._usePixmapCache and not QPixmapCache.find(key, pixmap):
            pixmap = QPixmap(clipRect.size())
            p = QPainter(pixmap)
            rect = QRect(0, 0, clipRect.width(), clipRect.height())
        
        base = self.baseColor
        grad = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.bottomLeft()))
        grad.setColorAt(0, self.highlightColor.lighter(120))
        if rect.height() == self.navigationWidgetHeight:
            grad.setColorAt(0.4, self.highlightColor)
            grad.setColorAt(0.401, base)
        grad.setColorAt(1, self.shadowColor)
        p.fillRect(rect, grad)
        
        shadowGradient = QLinearGradient(QPointF(spanRect.topLeft()), QPointF(spanRect.topRight()))
        shadowGradient.setColorAt(0, QColor(0, 0, 0, 30))
        highlight = self.highlightColor.lighter(130)
        highlight.setAlpha(100)
        shadowGradient.setColorAt(0.7, highlight)
        shadowGradient.setColorAt(1, QColor(0, 0, 0, 40))
        p.fillRect(rect, shadowGradient)
    
        if self._usePixmapCache and not QPixmapCache.find(key, pixmap):
            painter.drawPixmap(clipRect.topLeft(), pixmap)
            p.end()
            del p
            QPixmapCache.insert(key, pixmap)
        
    def menuGradient(self, painter, spanRect, clipRect):
        pass
    
    def mergedColors(self, colorA, colorB, factor = 50):
        maxFactor = 100
        color = QColor(colorA)
        return color
        
    def _initTheme(self):
        self.borderColor = QColor(self._baseColor)
        self.borderColor.setHsv(self._baseColor.hue(),
                                self._baseColor.saturation(),
                                self._baseColor.value()/2)
        self.shadowColor = QColor(self._baseColor)
        self.shadowColor.setHsv(self._baseColor.hue(),
                                clamp(self._baseColor.saturation() * 1.1),
                                clamp(self._baseColor.value() * 0.70))
        self.highlightColor = QColor(self._baseColor)
        self.highlightColor.setHsv(self._baseColor.hue(),
                                clamp(self._baseColor.saturation()),
                                clamp(self._baseColor.value() * 1.16))

theme = Theme()
