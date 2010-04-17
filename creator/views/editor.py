# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import log
from creator.config import CONF, get_font
from PyQt4.Qsci import (QsciScintilla, QsciAPIs, QsciLexerCPP, QsciLexerCSS,
                        QsciLexerDiff, QsciLexerHTML, QsciLexerPython,
                        QsciLexerProperties, QsciLexerBatch, QsciPrinter,
                        QsciLexerXML, QsciLexerYAML, QsciLexerSQL, QsciLexerJavaScript,
                        QsciLexerJava, QsciLexerLua)
from creator.utils import sourcecode


class CodeEditor(QsciScintilla):
    LEXERS = {
              ('py', 'pyw', 'python'): (QsciLexerPython, '#'),
              ('diff', 'patch', 'rej'): (QsciLexerDiff, ''),
              'css': (QsciLexerCSS, '#'),
              ('htm', 'html'): (QsciLexerHTML, ''),
              ('c', 'cpp', 'h'): (QsciLexerCPP, '//'),
              ('bat', 'cmd', 'nt'): (QsciLexerBatch, 'rem '),
              ('properties', 'session', 'ini', 'inf', 'reg', 'url',
               'cfg', 'cnf', 'aut', 'iss'): (QsciLexerProperties, '#'),
              ('java'): (QsciLexerJava, '//'),
              ('lua'): (QsciLexerLua, '--'),
              ('xml'): (QsciLexerXML, ''),
              ('yaml'): (QsciLexerYAML, ''),
              ('sql'): (QsciLexerSQL, ''),
              ('js'): (QsciLexerJavaScript, '//'),
              }
    TAB_ALWAYS_INDENTS = ('py', 'pyw', 'python', 'c', 'cpp', 'h')
    OCCURENCE_INDICATOR = QsciScintilla.INDIC_CONTAINER
    EOL_MODES = {"\r\n": QsciScintilla.EolWindows,
                 "\n":   QsciScintilla.EolUnix,
                 "\r":   QsciScintilla.EolMac}
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
    
    def setup_editor(self, linenumbers=True, language=None,
                     code_analysis=False, code_folding=False,
                     show_eol_chars=False, show_whitespace=False,
                     font=None, wrap=True, tab_mode=True):
        # Lexer
        self.set_language(language)
        
        if linenumbers:
            self.connect( self, SIGNAL('linesChanged()'), self.__lines_changed )
        self.setup_margins(linenumbers, code_analysis, code_folding)
        
        if font is not None:
            self.set_font(font)
        else:
            self.set_font(get_font('editor'))
        
    def setup_margins(self, linenumbers=True,
                      code_analysis=False, code_folding=False):
        """
        Setup margin settings
        (except font, now set in self.set_font)
        """
        for i_margin in range(5):
            # Reset margin settings
            self.setMarginWidth(i_margin, 0)
            self.setMarginLineNumbers(i_margin, False)
            self.setMarginMarkerMask(i_margin, 0)
            self.setMarginSensitivity(i_margin, False)
        if linenumbers:
            # 1: Line numbers margin
            self.setMarginLineNumbers(1, True)
            self.update_line_numbers_margin()
            if code_analysis:
                # 2: Errors/warnings margin
                mask = (1 << self.error) | (1 << self.warning)
                self.setMarginSensitivity(0, True)
                self.setMarginMarkerMask(0, mask)
                self.setMarginWidth(0, 14)
                self.connect(self,
                     SIGNAL('marginClicked(int,int,Qt::KeyboardModifiers)'),
                     self.__margin_clicked)
        if code_folding:
            # 0: Folding margin
            self.setMarginWidth(2, 14)
            self.setFolding(QsciScintilla.BoxedFoldStyle)                
        # Colors
        fcol = CONF.get('scintilla', 'margins/foregroundcolor')
        bcol = CONF.get('scintilla', 'margins/backgroundcolor')
        if fcol:
            self.setMarginsForegroundColor(QColor(fcol))
        if bcol:
            self.setMarginsBackgroundColor(QColor(bcol))
        fcol = CONF.get('scintilla', 'foldmarginpattern/foregroundcolor')
        bcol = CONF.get('scintilla', 'foldmarginpattern/backgroundcolor')
        if fcol and bcol:
            self.setFoldMarginColors(QColor(fcol), QColor(bcol))
            
    def set_language(self, language):
        self.supported_language = False
        self.comment_string = ''
        if language is not None:
            for key in self.LEXERS:
                if language.lower() in key:
                    self.supported_language = True
                    lexer_class, comment_string = self.LEXERS[key]
                    self.comment_string = comment_string
                    if lexer_class is not None:
                        # Fortran lexers are sometimes unavailable:
                        # the corresponding class is then replaced by None
                        # (see the import lines at the beginning of the script)
                        self.setLexer( lexer_class(self) )
                    break
                
    def is_python(self):
        return isinstance(self.lexer(), QsciLexerPython)
        
    def set_font(self, font):
        """Set shell font"""
        if self.lexer() is None:
            self.setFont(font)
        else:
            self.lexer().setFont(font)
            self.setLexer(self.lexer())
        self.setMarginsFont(font)
        
    def set_text(self, text):
        """Set the text of the editor"""
        self.setText(text)
        self.set_eol_mode(text)

    def get_text(self):
        """Return editor text"""
        return self.text()

    def __lines_changed(self):
        """Update margin"""
        self.update_line_numbers_margin()
        
    def update_line_numbers_margin(self):
        """Update margin width"""
        width = log(self.lines(), 10) + 2
        self.setMarginWidth(1, QString('0'*int(width)))