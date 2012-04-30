# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from app import Consts
from viewmanager import ViewManager
import creator_rc
import app
from fancy import Splitter, StatusBar

class Perspective:
    def __init__(self, window):
        self._window = window
        self._stage = QWidget()
        self._viewmanager = ViewManager()
        app.views = self._viewmanager
        self._initUi()
        self._window.setCentralWidget(self._stage)
    
    def _initUi(self):
        self._splitter = Splitter()
        
        splitter = Splitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.insertWidget(0, self._viewmanager.getView('editor'))
        splitter.setStretchFactor(0, 4)
        
        self._splitter.insertWidget(0, self._viewmanager.getView('navigation'))
        self._splitter.insertWidget(1, splitter)
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 2)
        
        self._statusBar = StatusBar()
        self._statusBar.setSizeGripEnabled(False)
        self._statusBar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        vlayout.setSpacing(0)
        vlayout.addWidget(self._splitter)
        vlayout.addWidget(self._statusBar)
        
        self._stage.setLayout(vlayout)
        