# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import fancy_rc

elementsSvgIds = ['ButtonBase', 
                  'ButtonNormalBase',
                  'ButtonNormalOverlay',
                  'ButtonPressedBase',
                  'ButtonPressedOverlay', 
                  'ButtonDisabledOverlay',
                  'ButtonHoverOverlay']

class ActionButton(QToolButton):
    _buttonElements = {}
    def __init__(self, parent=None):
        super(ActionButton, self).__init__(parent)
        self.setAttribute(Qt.WA_Hover, True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._buildButtonElements()
    
    def _buildButtonElements(self):
        if len(self._buttonElements) > 0: return
        from PyQt4.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(':/fancy/images/fancytoolbutton.svg')
        for id in elementsSvgIds:
            picture = QPicture()
            painter = QPainter(picture)
            renderer.render(painter, id)
            self._buttonElements[id] = picture
            
    def paintEvent(self, event):
        p = QPainter(self)
        sh = self.sizeHint()
        scale = (self.height()*1.0)/sh.height()
        if scale < 1:
            p.save()
            p.scale(1, scale)
        
        p.drawPicture(0, 0, self._buttonElements['ButtonBase'])
        status = 'ButtonPressedBase' if self.isDown() else 'ButtonNormalBase'
        p.drawPicture(0, 0, self._buttonElements[status])
        
        if scale < 1:
            p.restore()
        if not self.icon().isNull():
            self.icon().paint(p, self.rect())
        else:
            margin = 4
            p.drawText(self.rect().adjusted(margin, margin, -margin, -margin), 
                                 Qt.AlignCenter + Qt.TextWordWrap, self.text())
        
        if scale < 1:
            p.scale(1, scale)
        
        if self.isEnabled():
            status = 'ButtonPressedOverlay' if self.isDown() else 'ButtonNormalOverlay'
        else:
            status = 'ButtonDisabledOverlay'
        p.drawPicture(0, 0, self._buttonElements[status])
    
    def sizeHint(self):
        return self._buttonElements['ButtonBase'].boundingRect().size()
        
    def minimumSizeHint(self):
        return QSize(8,8)
    
    
class ActionBar(QWidget):
    def __init__(self, parent=None):
        super(ActionBar, self).__init__(parent)
        self._actionsLayout = QVBoxLayout()
        centeringLayout = QHBoxLayout()
        centeringLayout.addStretch()
        centeringLayout.addLayout(self._actionsLayout)
        centeringLayout.addStretch()
        self.setLayout(centeringLayout)
        
    def paintEvent(self, event):
        pass
    
    def insertAction(self, index, action, menu = None):
        toolButton = ActionButton(self)
        toolButton.setDefaultAction(action)
        if menu:
            toolButton.setMenu(menu)
            toolButton.setPopupMode(QToolButton.DelayedPopup)
            QObject.connect(toolButton, SIGNAL('triggered(QAction*)'),
                    self.toolButtonContextMenuTriggered)
        self._actionsLayout.insertWidget(index, toolButton)
    
    def toolButtonContextMenuTriggered(self, action):
        button = QObject.sender()
        if isinstance(button, QToolButton):
            if action != button.defaultAction():
                button.defaultAction().trigger()                