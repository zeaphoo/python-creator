# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:58:23 2009

@author: zhuowei
"""
from PyQt4 import QtCore, QtGui
from fancy import Splitter, TabWidget
from PyQt4.QtGui import *
from perspective import Perspective

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._menubar = QtGui.QMenuBar(self)
        self._menubar.addMenu('test')
        self.setMenuBar(self._menubar)
        self.modeStack = TabWidget(self)
        self.perspective = Perspective(self, self.modeStack)
        self.setCentralWidget(self.modeStack)
        
    
