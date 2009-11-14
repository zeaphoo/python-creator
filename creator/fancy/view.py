# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from styledbar import StyledBar
from button import ToolButton
from combobox import ComboBox

import fancy_rc

class View(QWidget):
    sigCloseView = SIGNAL('closeView(QString)')
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
        
        QObject.connect(close, SIGNAL('clicked()'), self.closeMe)
    
    def setParentView(self, view):
        self._parentView = view
    
    def getParentView(self):
        return self._parentView
        
    parentView = property(getParentView, setParentView)
    
    def closeMe(self):
        if sef.parentView:
            self.parentView.closeChildView(self)

