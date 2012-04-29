# -*- coding: utf-8 -*-

from fancy import ActionBar, Splitter
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from consts import Consts
from viewmanager import ViewManager
import creator_rc
import app
from fancy import Splitter, TabWidget

class Perspective:
    def __init__(self, window):
        self._window = window
        self._panel = TabWidget(self._window)
        self._actionBar = ActionBar(self._panel)
        self._viewmanager = ViewManager()
        app.views = self._viewmanager
        self._panel.addCornerWidget(self._actionBar)
        self._initUi()
        self._window.setCentralWidget(self._panel)
    
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
        
        # init all perpective views
        self._panel.insertTab(0, self._splitter, QIcon(Consts.icon_perspective_edit), 'Edit')
        # init global action
        #actRun = QAction(QIcon(Consts.icon_run), 'Run', None)
        #self.addAction(0, actRun)
        
    def addAction(self, pos, action):
        self._actionBar.insertAction(pos, action)
        