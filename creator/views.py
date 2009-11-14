# -*- coding: utf-8 -*-

from fancy import Navigation, EditorView
from PyQt4.QtGui import QWidget

class ViewManager:
    def __init__(self):
        self._views = {}
        self._factorys = {}
        self._initViews()
    
    def _initViews(self):
        nav = Navigation(self)
        self._views['navigation'] = nav
        ed = EditorView()
        self._views['editor'] = ed
        
        
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
