# -*- coding: utf-8 -*-

from fancy import Navigation, EditorView
from PyQt4.QtGui import QWidget
from views import FileSystemView, CodeEditor

class NavigationViewsManager:
    def __init__(self):
        self._views = []
        self._views.append(FileSystemView())
        
    def getSubWidget(self, index):
        return self._views[0]
        
class ViewManager:
    def __init__(self):
        self._views = {}
        self._factorys = {}
        self._initViews()
    
    def _initViews(self):
        
        nav = Navigation(NavigationViewsManager())
        self._views['navigation'] = nav
        ed = EditorView(None, CodeEditor)
        self._views['editor'] = ed
        txt = file('d:/img.py', 'rb').read()
        ed._widget.setText(txt)
        
        
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


