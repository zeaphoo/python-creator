# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:58:23 2009

@author: zhuowei
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSignal, QSize, QPoint, SIGNAL
from PyQt4.QtCore import Qt
from perspective import Perspective
from config import CONF, App_Name

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(App_Name)
        self._menubar = QtGui.QMenuBar(self)
        self._actions = {}
        self._handlers = {}
        self.buildActions()
        self.buildMenus()
        self.setMenuBar(self._menubar)
        self.perspective = Perspective(self)
    
    def setup(self):
        prefix = 'window/'
        width, height = CONF.get('main', prefix+'size')
        self.resize( QSize(width, height) )
        posx, posy = CONF.get('main', prefix+'position')
        self.move( QPoint(posx, posy) )
        # Is maximized?
        if CONF.get('main', prefix+'is_maximized'):
            self.setWindowState(Qt.WindowMaximized)
        # Is fullscreen?
        if CONF.get('main', prefix+'is_fullscreen'):
            self.setWindowState(Qt.WindowFullScreen)
        
    def closing(self):
        prefix = 'window'
        CONF.set('main', prefix+'/is_maximized', self.isMaximized())
        CONF.set('main', prefix+'/is_fullscreen', self.isFullScreen())
        if not self.isMaximized() and not self.isFullScreen():
            size = self.size()
            CONF.set('main', prefix+'/size', (size.width(), size.height()))
            pos = self.pos()
            CONF.set('main', prefix+'/position', (pos.x(), pos.y()))
        
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
    
    def closeEvent(self, event):
        self.closing()
        event.accept()
            
    def buildMenus(self):
        from menus import menus
        for m in menus:
            text = m['text']
            filem = self._menubar.addMenu(text)
            for a in m['menus']:
                if a == 'separator':
                    filem.addSeparator()
                else:
                    filem.addAction(self._actions[a])
        self.registerHandler('file_exit', self.exit)
        self.registerHandler('file_new', self.newFile)
        self.registerHandler('file_open', self.openFile)
        
    def buildActions(self):
        from actions import actions
        for key, value in actions.items():
            a = QAction(value['text'], self)
            a.setShortcut(QKeySequence(value['shortcut']))
            a.setData(unicode(key))
            a.triggered.connect(self.dispatchAction)
            self._actions[key] = a

    def dispatchAction(self, checked = False):
        action = self.sender()
        d = str(action.data().toString())
        if not self._handlers.has_key(d):
            print 'no handler for action', d
            return
        handler = self._handlers[d]
        handler()
        
    def registerHandler(self, name, handler):
        self._handlers[name] = handler
        
    def exit(self):
        QApplication.closeAllWindows()
        QApplication.processEvents()
        QApplication.exit()
    
    def newFile(self):
        ed = app.views.getView('editor')
        if ed is QWidget: return
        ed.newFile('untitiled.py', '#!/usr/bin/python\n# -*- coding: utf-8 -*-\n', 'py')
        
    def openFile(self):
        pass

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.setup()
    window.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
