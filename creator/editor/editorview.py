# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from creator.fancy import StyledBar, ToolButton, ComboBox
import os
import creator.fancy.fancy_rc
from creator.utils import encoding, random_key
from editor import CodeEditor

class EditorView(QWidget):
    def __init__(self, parent = None, editorWidget = None):
        super(EditorView, self).__init__(parent)
        self._toolBar = StyledBar(self)
        self._stack = QStackedWidget(self)
        self._widget = None
        if editorWidget is None:
            editorWidget = CodeEditor
        self._viewFactory = editorWidget
        self._pathWidgets = {}
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
        lay.addWidget(self._stack)
        
        self._navigationComboBox.currentIndexChanged.connect(self.activeEditor)
        close.clicked.connect(self.closeMe)
    
    @QtCore.pyqtSlot("bool")
    def closeMe(self, checked=False):
        index = self._navigationComboBox.currentIndex()
        newindex = index - 1
        if newindex < 0: newindex = 0
        self.removeEditor(index)
        if self._navigationComboBox.count() > 0:
            self._navigationComboBox.setCurrentIndex(newindex)
        
    def removeEditor(self, index):
        key = unicode(self._navigationComboBox.itemData(index).toPyObject())
        if self._pathWidgets.has_key(key):
            w = self._pathWidgets[key]
            self._pathWidgets.pop(key)
            self._stack.removeWidget(w)
        self._navigationComboBox.removeItem(index)
        
    
    def activeEditor(self, index):
        key = unicode(self._navigationComboBox.itemData(index).toPyObject())
        if self._pathWidgets.has_key(key):
            self._widget = self._pathWidgets[key]
            self._stack.setCurrentWidget(self._widget)
        
    def openFile(self, filepath):
        if self._pathWidgets.has_key(filepath):
            w = self._pathWidgets[filepath]
            index = self._navigationComboBox.findData(filepath)
            if index > -1 and index < self._navigationComboBox.count():
                self._navigationComboBox.setCurrentIndex(index)
        else:
            name = os.path.basename(filepath)
            w = self._viewFactory(self._stack)
            self._pathWidgets[filepath] = w
            self._widget = w
            self._stack.addWidget(w)
            self._navigationComboBox.addItem(name, QVariant(filepath))
            codefile = file(filepath, 'rb')
            self.setText(encoding.decode(codefile.read())[0])
            self.setup_editor(linenumbers=True, language=self._guessLanguage(filepath),
                                code_folding=True)
            self._navigationComboBox.setCurrentIndex(self._navigationComboBox.count()-1)
    
    def newFile(self, title, content, language):
        name = title
        filepath = 'tmp:///'+ random_key() + '/'+title
        w = self._viewFactory(self._stack)
        self._pathWidgets[filepath] = w
        self._widget = w
        self._stack.addWidget(w)
        self._navigationComboBox.addItem(name, QVariant(filepath))
        self.setText(unicode(content))
        self.setup_editor(linenumbers=True, language=language, code_folding=True)
        self._navigationComboBox.setCurrentIndex(self._navigationComboBox.count()-1)
    
    def _guessLanguage(self, filepath):
        ext = os.path.splitext(filepath)[1]
        return ext[1:]
        
    def __getattr__(self, name):
        if self._widget is not None:
            return getattr(self._widget, name)
        return None