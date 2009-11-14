# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 09:43:56 2009

@author: zhuowei
"""
from PyQt4 import QtCore, QtGui
import sys

app = QtGui.QApplication(sys.argv)
#style = QtGui.QStyleFactory.create("fancystyle")
#QtGui.QApplication.setStyle(style)

from creator import MainWindow
window = MainWindow()
window.show()
sys.exit(app.exec_())
