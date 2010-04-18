# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:43:56 2009

@author: zhuowei
"""
from PyQt4 import QtCore, QtGui
import sys

app = QtGui.QApplication(sys.argv)
from creator import MainWindow
window = MainWindow()
window.setup()
window.show()
sys.exit(app.exec_())
