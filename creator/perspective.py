# -*- coding: utf-8 -*-

from fancy import ActionBar, Splitter
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from consts import Consts
from views import ViewManager
import creator_rc

class Perspective:
    def __init__(self, window, modeStack):
        self._window = window
        self._modeStack = modeStack
        self._actionBar = ActionBar(modeStack)
        self._viewmanager = ViewManager()
        self._modeStack.addCornerWidget(self._actionBar)
        self._initUi()
    
    def _initUi(self):
        self._editPerspective = EditPerspective(self._viewmanager)
        # init all perpective views
        self._modeStack.insertTab(0, self._editPerspective.getWidget(), QIcon(Consts.icon_perspective_edit), 'Edit')
        self._modeStack.insertTab(1, QWidget(), QIcon(Consts.icon_perspective_debug), 'Debug')
        self._modeStack.insertTab(2, QWidget(), QIcon(Consts.icon_perspective_output), 'Output')
        # init global action
        #actDebug = QAction(QIcon(Consts.icon_debug), 'Debug', None)
        #self.addAction(0, actDebug)
        actRunSection = QAction(QIcon(Consts.icon_run_section), 'Run Selected Code', None)
        self.addAction(0, actRunSection)
        actRun = QAction(QIcon(Consts.icon_run), 'Run', None)
        self.addAction(0, actRun)
        
    def addAction(self, pos, action):
        self._actionBar.insertAction(pos, action)
        

class EditPerspective:
    def __init__(self, appviews):
        self._views = appviews
        self._splitter = Splitter()
        
        splitter = Splitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.insertWidget(0, self._views.getView('editor'))
        splitter.insertWidget(1, self._views.getView('output'))
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 0)
        
        self._splitter.insertWidget(0, self._views.getView('navigation'))
        self._splitter.insertWidget(1, splitter)
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        
    def getWidget(self):
        return self._splitter
        