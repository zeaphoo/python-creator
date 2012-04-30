# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QRect, pyqtSignal, QObject
from PyQt4.QtGui import QWidget, QPainter, QColor
from base import ToolButton, ComboBox
import fancy_rc
from theme import theme
from base import Splitter


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


class VerticalSplitView(Splitter):
    def __init__(self, parent = None):
        super(VerticalSplitView, self).__init__(parent)
        self._subViews = []
        self._widgetNames = []
        self._rawWidgets = {}
        self.setOrientation(Qt.Vertical)
    
    def initView(self, widgets=[], showdefault=False):
        self._widgetNames=[v[0] for v in widgets]
        self._rawWidgets.update(dict(widgets))
        if showdefault:
            self.showView(self._widgetNames[:1])
    
    def showView(self, names):
        for name in names:
            if name not in self._rawWidgets: 
                continue
            self.addView(name)
            
    def getView(self, name):
        if name in self._rawWidgets:
            return self._rawWidgets[name]
        return QWidget
            
    @property
    def allViewNames(self):
        return self._widgetNames
    
    def addView(self, name):
        ns = VerticalSplitElementView(self, name)
        ns.splitMe.connect(self.spliteView)
        ns.closeMe.connect(self.closeView)
        self.addWidget(ns)
        self._subViews.append((name, ns))
        return ns
        
    def insertView(self, pos, name):
        ns = VerticalSplitElementView(self, name)
        ns.splitMe.connect(self.spliteView)
        ns.closeMe.connect(self.closeView)
        self.insertWidget(pos, ns)
        self._subViews.insert(pos, (name, ns))
        return ns
    
    def spliteView(self, view):
        pos = self.indexOf(view)
        self.insertView(pos, view.viewName)
    
    def closeView(self, view):
        if len(self._subViews) != 1:
            self._subViews.remove((view.viewName, view))
            view.hide()
            view.deleteLater()


class VerticalSplitElementView(QWidget):
    splitMe = pyqtSignal('QWidget')
    closeMe = pyqtSignal('QWidget')
    def __init__(self, parent = None, name=None):
        super(VerticalSplitElementView, self).__init__(parent)
        self._view = parent
        self._selection = ComboBox(self)
        index = self._view.allViewNames.index(name)
        for itemname in self._view.allViewNames:
            self._selection.addItem(unicode(itemname))
        self._toolBar = StyledBar(self)
        self._widget = self._view.getView(name)(self)
        self._name = name
        toolBarLayout = QHBoxLayout()
        toolBarLayout.setMargin(0)
        toolBarLayout.setSpacing(0)
        self._toolBar.setLayout(toolBarLayout)
        toolBarLayout.addWidget(self._selection)
        
        splitAction = ToolButton()
        splitAction.setIcon(QIcon(":/fancy/images/splitbutton_horizontal.png"))
        splitAction.setToolTip("Split")
        close = ToolButton()
        close.setIcon(QIcon(":/fancy/images/closebutton.png"))
        close.setToolTip("Close")
    
        toolBarLayout.addWidget(splitAction)
        toolBarLayout.addWidget(close)
    
        lay = QVBoxLayout()
        lay.setMargin(0)
        lay.setSpacing(0)
        self.setLayout(lay);
        lay.addWidget(self._toolBar)
        lay.addWidget(self._widget)
    
        splitAction.clicked.connect(lambda: self.splitMe.emit(self) )
        close.clicked.connect(lambda: self.closeMe.emit(self))
        self._selection.activated.connect(self.setCurrentIndex)
        self._selection.setCurrentIndex(index)
    
    @property
    def viewName(self):
        return self._name
        
    def setCurrentIndex(self, index):
        widget = self._view.getView(self._selection.itemText(index))()
        self.layout().removeWidget(self._widget)
        self.layout().addWidget(widget)
        self._widget = widget
    
    def setFocusWidget(self):
        if self._widget:
            self._widget.setFocus()
            

class View(QWidget):
    sigCloseView = pyqtSignal('QString', name='closeView')
    def __init__(self, parent = None):
        super(View, self).__init__(parent)
        self._toolBar = StyledBar(self)
        self._parentView = None
        toolBarLayout = QHBoxLayout()
        toolBarLayout.setMargin(0)
        toolBarLayout.setSpacing(0)
        self._toolBar.setLayout(toolBarLayout)
        self._navigationComboBox = ComboBox(self)
        toolBarLayout.addWidget(self._navigationComboBox)
        
        close = ToolButton()
        close.setIcon(QIcon(":/fancy/images/closebutton.png"))
        close.setToolTip("Close")
        toolBarLayout.addWidget(close);
        
        lay = QVBoxLayout()
        lay.setMargin(0)
        lay.setSpacing(0)
        self.setLayout(lay)
        lay.addWidget(self._toolBar)
        
        close.clicked.connect(self.closeMe)
    
    def setParentView(self, view):
        self._parentView = view
    
    def getParentView(self):
        return self._parentView
        
    parentView = property(getParentView, setParentView)
    
    def closeMe(self):
        if sef.parentView:
            self.parentView.closeChildView(self)
            