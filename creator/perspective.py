# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
import app
from fancy import Splitter, StatusBar, VerticalSplitView
from editor import EditorView
from views import FileSystemView
        
class ViewManager:
    def __init__(self):
        self._views = {}
        self._factorys = {}
        self._initViews()
    
    def _initViews(self):
        self._views['filesystem'] = FileSystemView()
        self._views['editor'] = EditorView(None)
        
    def getView(self, name):
        if not self._views.has_key(name):
            return QWidget()
        return self._views[name]
        
    def registerView(self, name, view):
        if self._views.has_key(name):
            return
        self._views[name] = view
        
    def registerFactory(self, name, factory):
        return

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
        
        siderview = VerticalSplitView()
        siderview.initView([('filesystem', FileSystemView)],
                            showdefault = True)
        
        self._splitter.insertWidget(0, siderview)
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
        