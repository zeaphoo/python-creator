# -*- coding: utf-8 -*-
import os
import string
from PyQt4 import QtGui, QtCore
from highlighter import GenericHighlighter

class SyntaxEditor(QtGui.QPlainTextEdit):
    ## CODECS
    _codecs = { "utf8"  : "UTF-8",
                "CP1252": "Windows-1252",
                    }
    _occurences = 0

    def __init__(self, parent=None):
        QtGui.QPlainTextEdit.__init__(self, parent)
        self.parent = parent
        
        ## EXTENSION MANAGEMENT
        self.default_extension = '.py'
        
        #self.doc = QtGui.QTextDocument(self)
        self.tab_long = 4
        self.setTabEditorWidth(self.tab_long)

        self.line_col = QtGui.QColor("#502F2F")
        self.limit_color = QtGui.QColor("#C0000F")

        ## context :
        self.context = None

        ## highlighter
        self.highlighter = None
        self.findHighlighter()
        
        self.indent = 0

        ## Callbacks for paintEvent in plugins
        self.paint_callbacks=[]

        ## Customizations : show spaces, hilight current line, limit line
        self.showSpaces = False
        self.highlightCurrentLine = 0
        self.LimitLine = 79
        self.applyDefaultSettings()
        ## SIGNALS-SLOTS
        # for paintEvent
        self.connect( self.verticalScrollBar(),
                    QtCore.SIGNAL( "valueChanged(int)" ),
                    QtCore.SLOT("update()") )
        self.connect( self,
                    QtCore.SIGNAL( "textChanged()" ),
                    QtCore.SLOT("update()") )
    
    def setText(self, text):
        return self.setPlainText(text)
        
    def getText(self):
        return unicdoe(self.toPlainText())
        
    ## =========================
    ## Contexts management
    ## =========================
    def getContext(self):
        ext = self.get_fileExtension()
        return ext

    def closeEvent(self, event):
        pass

    def isModified(self):
        return self.document().isModified()

    def setTabEditorWidth(self,tw):
        self.setTabStopWidth( self.fontMetrics().width( "x" ) * tw )

    ## Text editing
    def getCursorPosition(self, para, index):
        i = 0
        p = self.document().begin()
        while p.isValid() :
            if para == i :
                break
            i += 1
            p = p.next()
        return p.position()+index

    def setCursorPosition(self, para, index):
        pos = self.getCursorPosition(para,index)
        cur = self.textCursor()
        cur.setPosition(pos,QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cur)
        self.ensureCursorVisible()
        self.setFocus()

    def numberOfLines(self):
        return self.document().blockCount()

    def gotoLine(self,line):
        #if line <= self.numberOfLines():
        self.setCursorPosition(line, 0)

    ## ===== Taken from Mark Summerfield's SanBox application
    def _walkTheLines(self, insert, text):
        userCursor = self.textCursor()
        userCursor.beginEditBlock()
        start = userCursor.position()
        end = userCursor.anchor()
        if start > end:
            start, end = end, start
        block = self.document().findBlock(start)
        while block.isValid():
            cursor = QtGui.QTextCursor(block)
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            if insert:
                cursor.insertText(text)
            else:
                cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                        QtGui.QTextCursor.KeepAnchor, len(text))
                if cursor.selectedText() == text:
                    cursor.removeSelectedText()
            block = block.next()
            if block.position() > end:
                break
        userCursor.endEditBlock()

    def indentRegion(self):
        self._walkTheLines(True, " " * self.tab_long)

    def unindentRegion(self):
        self._walkTheLines(False, " " * self.tab_long)

    ## ===== end of M.S SanBox application

    def getLineNumber(self):
        return self.textCursor().blockNumber() + 1

    def getColumnNumber(self):
        return self.textCursor().columnNumber() + 1

    def getlineNumberFromBlock(self, b):
        lineNumber = 1;
        block = self.document().begin()
        while block.isValid() and block != b:
            lineNumber += 1
            block = block.next()
        return lineNumber + 1

    def selectLines(self, debut, fin):
        if debut > fin :
            debut, fin = fin, debut
        c = self.textCursor()
        c.movePosition(QtGui.QTextCursor.Start )
        c.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor, debut-1 )
        c.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.KeepAnchor, fin-debut+1 )
        self.setTextCursor( c )
        self.ensureCursorVisible()

    ## ================== Ctrl+ MouseWheel for changing font size
    def wheelEvent(self, e):
        if e.modifiers() and QtCore.Qt.ControlModifier :
            delta = e.delta()
            if delta > 0:
                self.zoomOut(1)
            elif delta < 0:
                self.zoomIn(1)
            #self.parent.viewport().update()
            return
        QtGui.QAbstractScrollArea.wheelEvent(self,e)
        self.updateMicroFocus()
        #self.viewport().update()

    def currentLine(self):
        """Return the current edited line
        """
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        return cursor.selectedText()

    def findHighlighter(self, extGiven=False):
        """Tries to guess the highlighting from
        the extension.
        """
        lang = 'python'
        if self.highlighter :
            self.highlighter.changeRules(lang)
        else:
            self.highlighter = GenericHighlighter(self.document(), lang)
            print 'highlighter', self.highlighter
        self.highlighter.rehighlight()

    ## ======================================== Settings
    def applyDefaultSettings(self):
        self.applySettings('#444031','#DBD6C1','DejaVu Sans Mono',11,'#CE5C00','#2E3436')

    def applySettings(self,fgcolor,bgcolor,fontfam,fontsize,lfgcolor,lbgcolor):
        palette = QtGui.QPalette()
        # Palette
        brush = QtGui.QBrush(QtGui.QColor(fgcolor))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(bgcolor))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(fgcolor))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(bgcolor))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(180,180,180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.HighlightedText,brush)

        brush = QtGui.QBrush(QtGui.QColor(180,180,180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(170,250,124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.HighlightedText,brush)

        brush = QtGui.QBrush(QtGui.QColor(217,217,217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.HighlightedText,brush)

        self.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily(fontfam)
        font.setPointSize(fontsize)
        self.setFont(font)
#        if self.highlighter :
#            self.parent.lines.fg_color = QtGui.QColor(lfgcolor)
#            self.parent.lines.applyBackgroundColor(QtGui.QColor(lbgcolor))

    def paintEvent(self, event):

        painter = QtGui.QPainter(self.viewport())

        # CurrentLine background
        if self.highlightCurrentLine:
            r = self.cursorRect()
            r.setX(0) #Sets the left edge of the rectangle to the given coordinate.
            r.setWidth( self.viewport().width() )

            painter.fillRect( r, QtGui.QBrush( self.line_col ) )
            painter.setPen( self.limit_color )
            painter.drawRect( r )

            #painter.setPen( self.limit_color )
            #painter.drawRoundRect ( r )

        # LimitLine
        if self.LimitLine > 0:
            x = ( QtGui.QFontMetrics( self.font() ).width( "X" ) * self.LimitLine ) - self.horizontalScrollBar().value()
            painter.setPen( self.limit_color )
            painter.drawLine( x, painter.window().top(), x, painter.window().bottom() )
        painter.end()

        # Tabs and spaces
        if self.showSpaces :
            pass #self.printWhiteSpaces(event)

        # Callbacks from plugins
        if self.paint_callbacks :
            for pc in self.paint_callbacks:
                pc.paint(event)
        QtGui.QPlainTextEdit.paintEvent(self,event)
    