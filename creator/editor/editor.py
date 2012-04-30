# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import log
from creator.config import CONF, get_font
from creator.utils import sourcecode
from syntaxeditor import SyntaxEditor


class CodeEditor(SyntaxEditor):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        
    def set_text(self, text):
        """Set the text of the editor"""
        self.setText(text)

    def get_text(self):
        """Return editor text"""
        return self.text()
        
    def setup_editor(self, linenumbers=True, language=None,
                     code_analysis=False, code_folding=False,
                     show_eol_chars=False, show_whitespace=False,
                     font=None, wrap=True, tab_mode=True):
        pass