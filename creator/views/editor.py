# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4.Qsci import (QsciScintilla, QsciAPIs, QsciLexerCPP, QsciLexerCSS,
                        QsciLexerDiff, QsciLexerHTML, QsciLexerPython,
                        QsciLexerProperties, QsciLexerBatch, QsciPrinter)
                        

class CodeEditor(QsciScintilla):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        self.setup()
        
    
    def setup(self):
        """Configure Scintilla"""
        # UTF-8
        self.setUtf8(True)
        
        # Indentation
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setTabIndents(True)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)
        
        # Enable brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(Qt.yellow)