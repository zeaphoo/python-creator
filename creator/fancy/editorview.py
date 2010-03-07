# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from styledbar import StyledBar
from button import ToolButton
from combobox import ComboBox

import fancy_rc

class EditorView(QWidget):
    def __init__(self, parent = None, editorWidget = None):
        super(EditorView, self).__init__(parent)
        self._toolBar = StyledBar(self)
        if editorWidget is None:
            editorWidget = QWidget
        self._widget = editorWidget(self)
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
        lay.addWidget(self._widget)
        
        QObject.connect(close, SIGNAL('clicked()'), self.closeMe)
        
    def closeMe(self):
        pass
