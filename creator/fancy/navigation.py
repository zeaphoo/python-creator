# -*- coding: utf-8 -*-

from splitter import Splitter
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from styledbar import StyledBar
from combobox import ComboBox
from button import ToolButton

import fancy_rc


class Navigation(Splitter):
    def __init__(self, factory, parent = None):
        super(Navigation, self).__init__(parent)
        self._subWidgets = []
        self._factory = factory
        self.setOrientation(Qt.Vertical)
        self.insertSub(0)
        
    
    def insertSub(self, pos):
        ns = NavigationSub(self._factory, self)
        QObject.connect(ns, SIGNAL('spliteMe()'), self.spliteSub)
        QObject.connect(ns, SIGNAL('closeMe()'), self.closeSub)
        self.insertWidget(pos, ns)
        self._subWidgets.insert(pos, ns)
        return ns
    
    def spliteSub(self):
        sub = QObject.sender()
        pos = self.indexof(sub) + 1
        self.insertSub(pos)
    
    def closeSub(self):
        if len(self._subWidgets) != 1:
            sub = QObject.sender()
            self._subWidgets.remove(sub)
            sub.hide()
            sub.deleteLater()
        else:
            self.setShown(False)
    
    def setShown(self, show):
        if show == self.visible():
            return
        self.setVisible(show)

class NavigationSub(QWidget):
    splitMe = SIGNAL('splitMe()')
    closeMe = SIGNAL('closeMe()')
    def __init__(self, factory, parent = None):
        super(NavigationSub, self).__init__(parent)
        self._navigationComboBox = ComboBox(self)
        self._navigationComboBox.addItem('test')
        self._navigationComboBox.addItem(u'测试')
        self._toolBar = StyledBar(self)
        self._widget = QWidget(self)
        toolBarLayout = QHBoxLayout()
        toolBarLayout.setMargin(0)
        toolBarLayout.setSpacing(0)
        self._toolBar.setLayout(toolBarLayout)
        self._navWidget = None
        self.factory = factory
        toolBarLayout.addWidget(self._navigationComboBox)
        
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
    
        QObject.connect(splitAction, SIGNAL('clicked()'), self, SIGNAL('splitMe()'))
        QObject.connect(close, SIGNAL('clicked()'), self, SIGNAL('closeMe()'))
        QObject.connect(self._navigationComboBox, SIGNAL('currentIndexChanged(int)'),
                self.setCurrentIndex)
    
    def setCurrentIndex(self, index):
        navigationWidget = self.factory.getSubWidget(index)
        if navigationWidget:
            self.layout().removeWidget(self._navWidget)
            self.layout().addWidget(navigationWidget)
            self._navWidget = navigationWidget
    
    def setFocusWidget(self):
        if self._navWidget:
            self._navWidget.setFocus()
    