# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:58:23 2009

@author: zhuowei
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, QVariant, SIGNAL, QString
from PyQt4.QtCore import Qt
from fancy import Splitter, TabWidget
from PyQt4.QtGui import *
from perspective import Perspective

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._menubar = QtGui.QMenuBar(self)
        self._actions = {}
        self._handlers = {}
        self.buildActions()
        self.buildMenus()
        self.setMenuBar(self._menubar)
        self.modeStack = TabWidget(self)
        self.perspective = Perspective(self, self.modeStack)
        self.setCentralWidget(self.modeStack)
        
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
        
    def buildActions(self):
        from actions import actions
        for key, value in actions.items():
            a = QAction(value['text'], self)
            a.setShortcut(QKeySequence(value['shortcut']))
            a.setData(QVariant(unicode(key)))
            QObject.connect(a, SIGNAL('triggered(bool)'), self.dispatchAction)
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
