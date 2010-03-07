# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path

class FileSystemModel(QDirModel):
    def __init__(self, parent=None):
        """
        Custom QDirModel with Drag & Drop support
        """
        self.parent = parent
        super(FileSystemModel, self).__init__(parent)

    def columnCount(self, index):
        return 1
        
    def flags(self, index):
        if index.isValid() and self.isDir(index):
            return Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled


class FileSystemView(QTreeView):
    def __init__(self, parent=None):
        super(FileSystemView, self).__init__(parent)
        
        self.model = FileSystemModel()
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.model.setSorting(QDir.DirsFirst)
        self.setModel(self.model)
        
    def mouseDoubleClickEvent(self, event):
        """Reimplement Qt method"""
        QTreeView.mouseDoubleClickEvent(self, event)
        self.clicked()
        
    def getSelectedPath(self):
        """Return selected filename"""
        index = self.currentIndex()
        if index:
            return os.path.normpath(unicode(self.model.filePath(index)))
        
    def clicked(self):
        fname = self.getSelectedPath()
        if fname:
            if os.path.isdir(fname):
                #self.parent.emit(SIGNAL("open_dir(QString)"), fname)
                self.refresh()
            else:
                self.open(fname)
                
    def open(self, name):
        fname = unicode(name)
        ext = os.path.splitext(fname)[1]
        print 'ext', ext
