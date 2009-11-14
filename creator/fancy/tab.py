# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QSizePolicy, QFont, QFontMetrics, QLinearGradient, QStatusBar
from PyQt4.QtGui import QPen, QVBoxLayout, QHBoxLayout, QStackedLayout, QPainter, QColor
from PyQt4.QtCore import *
from theme import theme
from statusbar import StatusBar
from styledbar import StyledBar

class FancyTab:
    icon = None
    text = None
    tooltip = None
    
class TabBar(QWidget):
    _rounding = 22
    def __init__(self, parent=None):
        super(TabBar, self).__init__(parent)
        self._currentIndex = 0
        self._hoverIndex = -1
        self._hoverControl = QTimeLine()
        self._tabs = []
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setMinimumWidth(max(2 * self._rounding, 40))
        self.setAttribute(Qt.WA_Hover, True)
        self.setFocusPolicy(Qt.NoFocus)
        self._hoverControl.setFrameRange(0, 20)
        self._hoverControl.setDuration(130)
        self._hoverControl.setCurveShape(QTimeLine.EaseInCurve)
        QObject.connect(self._hoverControl, SIGNAL('frameChanged(int)'), self.updateHover)
        self.setMouseTracking(True)
    
    def insertTab(self, index, icon, label):
        tab = FancyTab()
        tab.icon = icon
        tab.text = label
        self._tabs.insert(index, tab)
    
    def removeTab(self, index):
        self._tabs.remove(index)
        
    def setCurrentIndex(self, index):
        self._currentIndex = index
    
    def getCurrentIndex(self):
        return self._currentIndex
        
    currentIndex = property(getCurrentIndex, setCurrentIndex)
    
    def tabSizeHint(self, minimum = False):
        boldFont = QFont(self.font())
        boldFont.setPointSizeF(theme.sidebarFontSize)
        boldFont.setBold(True)
        fm = QFontMetrics(boldFont)
        spacing = 6
        width = 60 + spacing + 2
        iconHeight = 0 if minimum else 32
        return QSize(width, iconHeight + spacing + fm.height())
        
    def tabRect(self, index):
        sh = self.tabSizeHint()
        if sh.height() * len(self._tabs) > self.height():
            sh.setHeight(self.height() / len(self._tabs))
        return QRect(0, index * sh.height(), sh.width(), sh.height())
    
    def tabIcon(self, index):
        return self._tabs[index].icon
        
    def tabText(self, index):
        return self._tabs[index].text
        
    def sizeHint(self):
        sh = self.tabSizeHint()
        return QSize(sh.width(), sh.height() * len(self._tabs))
    
    def minimumSizeHint(self):
        sh = self.tabSizeHint(True)
        return QSize(sh.width(), sh.height() * len(self._tabs))
    
    def mousePressEvent(self, event):
        event.accept()
        for i in range(0, len(self._tabs)):
            if self.tabRect(i).contains(event.pos()):
                self._currentIndex = i
                break
        self.update()
    
    def mouseMoveEvent(self, event):
        if not self._hoverRect.contains(event.pos()):
            newHover = -1
            for i in range(0, len(self._tabs)):
                if self.tabRect(i).contains(event.pos()):
                    newHover = i
                    break
            self._hoverControl.stop()
            self._hoverIndex = newHover
            self.update(self._hoverRect)
            self._hoverRect = QRect()
            
            if self._hoverIndex  >= 0:
                oldHoverRect = self._hoverRect
                self._hoverRect = self.tabRect(self._hoverIndex)
                self._hoverControl.start()
    
    def updateHover(self, index):
        self.update(self._hoverRect)
        
    def enterEvent(self, event):
        self._hoverRect = QRect()
        self._hoverIndex = -1
    
    def leaveEvent(self, event):
        if self._hoverIndex >= 0:
            self._hoverIndex = -1
            self.update(self._hoverRect)
            self._hoverRect = QRect()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(0, len(self._tabs)):
            if i != self.currentIndex:
                self._paintTab(painter, i)
        if len(self._tabs) > 0:
            self._paintTab(painter, self.currentIndex)
    
    def _paintTab(self, painter, index):
        painter.save()
        rect = self.tabRect(index)
        selected = True if index == self.currentIndex else False
        hover = True if index == self._hoverIndex else False
        background = QColor(0, 0, 0, 10)
        if hover:
            hoverColor = QColor(255, 255, 255, self._hoverControl.currentFrame())
        light = QColor(255, 255, 255, 40)
        dark = QColor(0, 0, 0, 60)
        if selected:
            selectedGradient = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.center().x(), rect.bottom()))
            selectedGradient.setColorAt(0, Qt.white)
            selectedGradient.setColorAt(0.3, Qt.white)
            selectedGradient.setColorAt(0.7, QColor(230, 230, 230))
            
            painter.fillRect(rect, selectedGradient)
            painter.setPen(QColor(200, 200, 200))
            painter.drawLine(rect.topLeft(), rect.topRight())
            painter.setPen(QColor(150, 160, 200))
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        else:
            painter.fillRect(rect, background)
            if hover:
                painter.fillRect(rect, hoverColor);
            painter.setPen(QPen(light, 0))
            painter.drawLine(rect.topLeft(), rect.topRight())
            painter.setPen(QPen(dark, 0))
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        tabText = self.tabText(index)
        tabTextRect = QRect(self.tabRect(index))
        tabIconRect = QRect(tabTextRect)
        boldFont = QFont(painter.font())
        boldFont.setPointSizeF(theme.sidebarFontSize)
        boldFont.setBold(True)
        painter.setFont(boldFont)
        pencolor = theme.panelTextColor if selected else QColor(30, 30, 30, 80)
        painter.setPen(pencolor)
        textFlags = Qt.AlignCenter + Qt.AlignBottom + Qt.ElideRight + Qt.TextWordWrap
        painter.drawText(tabTextRect, textFlags, tabText)
        pencolor = QColor(60, 60, 60) if selected else theme.panelTextColor
        painter.setPen(pencolor)
        textHeight = painter.fontMetrics().boundingRect(
                        QRect(0, 0, self.width(), self.height()), Qt.TextWordWrap, tabText).height()
        tabIconRect.adjust(0, 4, 0, -textHeight)
        iconSize = min(tabIconRect.width(), tabIconRect.height())
        if iconSize > 4:
            self.style().drawItemPixmap(painter, tabIconRect, Qt.AlignCenter + Qt.AlignVCenter,
                                    self.tabIcon(index).pixmap(tabIconRect.size()))
        painter.translate(0, -1)
        painter.drawText(tabTextRect, textFlags, tabText)
        painter.restore()

class ColorButton(QWidget):
    def __init__(self, parent=None):
        super(ColorButton, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        
class TabWidget(QWidget):
    _tabBar = None
    _selectionWidget = None
    _cornerWidgetContainer = None
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self._tabBar = TabBar(self)
        self._selectionWidget = QWidget(self)
        selectionLayout = QVBoxLayout()
        selectionLayout.setSpacing(0)
        selectionLayout.setMargin(0)
        bar = StyledBar()
        layout = QHBoxLayout(bar)
        layout.setMargin(0)
        layout.setSpacing(0)
        selectionLayout.addWidget(bar)
        
        selectionLayout.addWidget(self._tabBar, 1)
        self._selectionWidget.setLayout(selectionLayout)
        self._selectionWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        self._cornerWidgetContainer = QWidget(self)
        self._cornerWidgetContainer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self._cornerWidgetContainer.setAutoFillBackground(False)
        
        cornerWidgetLayout = QVBoxLayout()
        cornerWidgetLayout.setSpacing(0)
        cornerWidgetLayout.setMargin(0)
        cornerWidgetLayout.addStretch()
        self._cornerWidgetContainer.setLayout(cornerWidgetLayout)
        
        selectionLayout.addWidget(self._cornerWidgetContainer, 0)
        self._modesStack = QStackedLayout()
        self._statusBar = StatusBar()
        self._statusBar.setSizeGripEnabled(False)
        self._statusBar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        vlayout.setSpacing(0)
        vlayout.addLayout(self._modesStack)
        vlayout.addWidget(self._statusBar)
        
        mainLayout = QHBoxLayout()
        mainLayout.setMargin(0)
        mainLayout.setSpacing(1)
        mainLayout.addWidget(self._selectionWidget)
        mainLayout.addLayout(vlayout)
        self.setLayout(mainLayout)
        
    def insertTab(self, index, tab, icon, label):
        self._modesStack.insertWidget(index, tab)
        self._tabBar.insertTab(index, icon, label)
    
    def removeTab(self, index):
        self._modesStack.removeWidget(self._modesStack.widget(index))
        self._tabBar.removeTab(index)
        
    def setCurrentIndex(self, index):
        self._tabBar.currentIndex = index
    
    def getCurrentIndex(self):
        return self._tabBar.currentIndex
        
    currentIndex = property(getCurrentIndex, setCurrentIndex)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self._selectionWidget.rect().adjusted(0, 0, 1, 0)
        rect = self.style().visualRect(self.layoutDirection(), self.geometry(), rect)
        theme.verticalGradient(painter, rect, rect)
        painter.setPen(theme.borderColor)
        painter.drawLine(rect.topRight(), rect.bottomRight())
    
    def addCornerWidget(self, widget):
        self._cornerWidgetContainer.layout().addWidget(widget)
    
    def insertCornerWidget(self, pos, widget):
        layout = self._cornerWidgetContainer.layout()
        layout.insertWidget(pos, widget)
    
    def cornerWidgetCount(self):
        return self._cornerWidgetContainer.layout().count()
        
    
