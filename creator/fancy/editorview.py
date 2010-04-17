# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from styledbar import StyledBar
from button import ToolButton
from combobox import ComboBox
import os
import fancy_rc
from creator.utils import encoding

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
        
    def openFile(self, filepath):
        codefile = file(filepath, 'rb')
        self.setText(encoding.decode(codefile.read())[0])
        self.setup_editor(linenumbers=True, language=self._guessLanguage(filepath),
                            code_folding=True)
    
    def _guessLanguage(self, filepath):
        ext = os.path.splitext(filepath)[1]
        return ext[1:]
        
    def __getattr__(self, name):
        return getattr(self._widget, name)