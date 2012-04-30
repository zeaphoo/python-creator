# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from theme import theme

import fancy_rc

class FancyStyle:
    def __init__(self):
        self.lineeditImage = QImage(":/fancy/images/inputfield.png");
        self.lineeditImage_disabled = QImage(":/fancy/images/inputfield_disabled.png");
    
    @property
    def style(self):
        return QtGui.QApplication.instance().style()
        
    def pixelMetric(self, metric, option = None, widget = None):
        retval = self.style.pixelMetric(metric, option, widget)
        if metric == QStyle.PM_ButtonShiftHorizontal or metric == QStyle.PM_ButtonShiftVertical:
            retval = 0
        return retval
        
    def panelPalette(self, oldPalette):
        color = QColor(theme.panelTextColor)
        pal = QPalette(oldPalette)
        pal.setBrush(QPalette.All, QPalette.WindowText, color)
        pal.setBrush(QPalette.All, QPalette.ButtonText, color)
        pal.setBrush(QPalette.All, QPalette.Foreground, color)
        color.setAlpha(100)
        pal.setBrush(QPalette.Disabled, QPalette.WindowText, color)
        pal.setBrush(QPalette.Disabled, QPalette.ButtonText, color)
        pal.setBrush(QPalette.Disabled, QPalette.Foreground, color)
        return pal
    
    def drawCornerImage(img, painter, rect, left = 0, top = 0, right = 0, bottom = 0):
        pass
    
    def draw_IndicatorArrowUp(self, opt, painter, widget):
        self._draw_IndicatorArrow(1, opt, painter, widget)
        
    def draw_IndicatorArrowDown(self, opt, painter, widget):
        self._draw_IndicatorArrow(2, opt, painter, widget)
        
    def draw_IndicatorArrowRight(self, opt, painter, widget):
        self._draw_IndicatorArrow(3, opt, painter, widget)
        
    def draw_IndicatorArrowLeft(self, opt, painter, widget):
        self._draw_IndicatorArrow(4, opt, painter, widget)
        
    def _draw_IndicatorArrow(self, direction, opt, painter, widget):
        if opt.rect.width() <= 1 or opt.rect.height() <= 1:
            return
        r = opt.rect
        size = min(r.height(), r.width())
        pixmap = QPixmap()
        pixmapName = "%s-%s-%d-%d-%d-%d" %(
                       "fancy", 'style', int(opt.state), direction,
                       size, opt.palette.cacheKey())
        if not QPixmapCache.find(pixmapName, pixmap):
            border = size/5
            sqsize = 2*(size/2)
            image = QImage(sqsize, sqsize, QImage.Format_ARGB32)
            image.fill(Qt.transparent)
            imagePainter = QPainter(image)
            imagePainter.setRenderHint(QPainter.Antialiasing, True)
            imagePainter.translate(0.5, 0.5)
            a = QPolygon()
            if direction == 1:
                a.setPoints(border, sqsize/2,  sqsize/2, border,  sqsize - border, sqsize/2)
            elif direction == 2:
                a.setPoints(border, sqsize/2,  sqsize/2, sqsize - border,  sqsize - border, sqsize/2)
            elif direction == 3:
                a.setPoints(sqsize - border, sqsize/2,  sqsize/2, border,  sqsize/2, sqsize - border)
            else:
                a.setPoints(border, sqsize/2,  sqsize/2, border,  sqsize/2, sqsize - border)
            bsx = 0
            bsy = 0
            if opt.state & QStyle.State_Sunken:
                bsx = self.pixelMetric(QStyle.PM_ButtonShiftHorizontal)
                bsy = self.pixelMetric(QStyle.PM_ButtonShiftVertical)
            bounds = a.boundingRect()
            sx = sqsize / 2 - bounds.center().x() - 1
            sy = sqsize / 2 - bounds.center().y() - 1
            imagePainter.translate(sx + bsx, sy + bsy)
            
            if not (opt.state & QStyle.State_Enabled):
                foreGround = QColor(150, 150, 150, 150)
                imagePainter.setBrush(opt.palette.mid().color())
                imagePainter.setPen(opt.palette.mid().color())
            else:
                shadow = QColor(0, 0, 0, 100)
                imagePainter.translate(0, 1)
                imagePainter.setPen(shadow)
                imagePainter.setBrush(shadow)
                foreGround = QColor(255, 255, 255, 210)
                imagePainter.drawPolygon(a)
                imagePainter.translate(0, -1)
                imagePainter.setPen(foreGround)
                imagePainter.setBrush(foreGround)
            imagePainter.drawPolygon(a)
            imagePainter.end()
            pixmap = QPixmap.fromImage(image)
            QPixmapCache.insert(pixmapName, pixmap)
        xOffset = r.x() + (r.width() - size)/2
        yOffset = r.y() + (r.height() - size)/2
        painter.drawPixmap(xOffset, yOffset, pixmap)
    
    def draw_PanelButtonTool(self, option, painter, widget):
        rect = option.rect
        pressed = option.state & QStyle.State_Sunken or option.state & QStyle.State_On
        shadow = QColor(0, 0, 0, 30)
        painter.setPen(shadow)
        if pressed:
            shade = QColor(0, 0, 0, 40)
            painter.fillRect(rect, shade)
            painter.drawLine(rect.topLeft() + QPoint(1, 0), rect.topRight() - QPoint(1, 0))
            painter.drawLine(rect.topLeft(), rect.bottomLeft())
            painter.drawLine(rect.topRight(), rect.bottomRight())
            highlight = QColor(255, 255, 255, 30)
            painter.setPen(highlight)
        elif option.state & QStyle.State_Enabled and option.state & QStyle.State_MouseOver:
            lighter = QColor(255, 255, 255, 37)
            painter.fillRect(rect, lighter)
        
    def draw_ComboBox(self, option, painter, widget):
        painter.save()
        rect = option.rect
        isEmpty = not option.currentText
        reverse = option.direction == Qt.RightToLeft
        
        grad = QLinearGradient(QPointF(option.rect.topRight()), QPointF(option.rect.bottomRight()))
        grad.setColorAt(0, QColor(255, 255, 255, 20))
        grad.setColorAt(0.4, QColor(255, 255, 255, 60))
        grad.setColorAt(0.7, QColor(255, 255, 255, 50))
        grad.setColorAt(1, QColor(255, 255, 255, 40))
        painter.setPen(QPen(grad, 0))
        painter.drawLine(rect.topRight(), rect.bottomRight())
        grad.setColorAt(0, QColor(0, 0, 0, 30))
        grad.setColorAt(0.4, QColor(0, 0, 0, 70))
        grad.setColorAt(0.7, QColor(0, 0, 0, 70))
        grad.setColorAt(1, QColor(0, 0, 0, 40))
        painter.setPen(QPen(grad, 0))
        if not reverse:
            painter.drawLine(rect.topRight() - QPoint(1,0), rect.bottomRight() - QPoint(1,0))
        else:
            painter.drawLine(rect.topLeft(), rect.bottomLeft())
        toolbutton = QStyleOption(option)
        if isEmpty:
            toolbutton.state &= ~(QStyle.State_Enabled | QStyle.State_Sunken)
        painter.save()
        painter.setClipRect(toolbutton.rect.adjusted(0, 0, -2, 0))
        self.draw_PanelButtonTool(toolbutton, painter, widget)
        painter.restore()
        #draw arrow
        menuButtonWidth = 12
        left = rect.right() - menuButtonWidth if not reverse else rect.left()
        right = rect.right() if not reverse else rect.left() + menuButtonWidth
        arrowRect = QRect((left + right) / 2 + ( 6 if reverse else -6), rect.center().y() - 3, 9, 9)
        if option.state & QStyle.State_On:
            arrowRect.translate(self.style.pixelMetric(QStyle.PM_ButtonShiftHorizontal, option, widget),
                                self.style.pixelMetric(QStyle.PM_ButtonShiftVertical, option, widget))

        arrowOpt = QStyleOption(option)
        arrowOpt.rect = arrowRect
        if isEmpty:
            arrowOpt.state &= ~(QStyle.State_Enabled | QStyle.State_Sunken)
            
        if self.style.styleHint(QStyle.SH_ComboBox_Popup, option, widget, None):
            arrowOpt.rect.translate(0, -3)
            self.draw_IndicatorArrowUp(arrowOpt, painter, widget)
            arrowOpt.rect.translate(0, 6)
            self.draw_IndicatorArrowDown(arrowOpt, painter, widget)
        else:
            self.draw_IndicatorArrowDown(arrowOpt, painter, widget)
        painter.restore()
    
    def draw_ComboBoxLabel(self, option, painter, widget):
        editRect = self.style.subControlRect(QStyle.CC_ComboBox, option, QStyle.SC_ComboBoxEditField, widget)
        customPal = option.palette

        if not option.currentIcon.isNull():
            mode = QIcon.Normal if option.state & State_Enabled else QIcon.Disabled
            pixmap = option.currentIcon.pixmap(option.iconSize, mode)
            iconRect = QRect(editRect)
            iconRect.setWidth(option.iconSize.width() + 4)
            iconRect = alignedRect(option.direction,
                                   Qt.AlignLeft | Qt.AlignVCenter,
                                   iconRect.size(), editRect)
            if option.editable:
                painter.fillRect(iconRect, customPal.brush(QPalette.Base))
            self.style.drawItemPixmap(painter, iconRect, Qt.AlignCenter, pixmap)
            
            if option.direction == Qt.RightToLeft:
                editRect.translate(-4 - option.iconSize.width(), 0)
            else:
                editRect.translate(option.iconSize.width() + 4, 0)
            editRect.adjust(0, 0, -13, 0)

        customPal.setBrush(QPalette.All, QPalette.ButtonText, QColor(0, 0, 0, 70))

        text = option.fontMetrics.elidedText(option.currentText, Qt.ElideRight, editRect.width())
        self.style.drawItemText(painter, editRect.translated(0, 1),
                     self.style.visualAlignment(option.direction, Qt.AlignLeft | Qt.AlignVCenter),
                     customPal, option.state & QStyle.State_Enabled, text, QPalette.ButtonText)
        customPal.setBrush(QPalette.All, QPalette.ButtonText, theme.panelTextColor)
        self.style.drawItemText(painter, editRect,
                     self.style.visualAlignment(option.direction, Qt.AlignLeft | Qt.AlignVCenter),
                     customPal, option.state & QStyle.State_Enabled, text, QPalette.ButtonText)
        
        
    def draw_ToolButton(self, option, painter, widget):
        rect = option.rect
        btnRect = self.style.subControlRect(QStyle.CC_ToolButton, option,
                                        QStyle.SC_ToolButton, widget)
        menuRect = self.style.subControlRect(QStyle.CC_ToolButton, option,
                                        QStyle.SC_ToolButtonMenu, widget)
        
        bflags = option.state
        if bflags & QStyle.State_AutoRaise:
            if not (bflags & QStyle.State_MouseOver):
                bflags &= ~QStyle.State_Raised
        
        mflags = QStyle.State(bflags)
        if option.state & QStyle.State_Sunken:
            if option.activeSubControls & QStyle.SC_ToolButton:
                bflags |= QStyle.State_Sunken
            if option.activeSubControls & QStyle.SC_ToolButtonMenu:
                mflags |= QStyle.State_Sunken
        
        tool = QStyleOption(0)
        tool.palette = option.palette
        if option.subControls & QStyle.SC_ToolButton:
            tool.rect = btnRect
            tool.state = bflags
            self.draw_PanelButtonTool(tool, painter, widget)

        if option.state & QStyle.State_HasFocus:
            fr = QStyleOptionFocusRect(option)
            fr.rect.adjust(3, 3, -3, -3)
            if option.features & QStyleOptionToolButton.MenuButtonPopup:
                fr.rect.adjust(0, 0, -self.pixelMetric(QStyle.PM_MenuButtonIndicator,
                                                  option, widget), 0)
            oldPen = painter.pen()
            focusColor = theme.panelTextColor
            focusColor.setAlpha(120)
            outline = QPen(focusColor, 1)
            outline.setStyle(Qt.DotLine)
            painter.setPen(outline)
            r = option.rect.adjusted(2, 2, -2, -2)
            painter.drawRect(r)
            painter.setPen(oldPen)
            
        label = QStyleOptionToolButton(option)
        label.palette = self.panelPalette(option.palette)
        fw = self.pixelMetric(QStyle.PM_DefaultFrameWidth, option, widget)
        label.rect = btnRect.adjusted(fw, fw, -fw, -fw)
        self.style.drawControl(QStyle.CE_ToolButtonLabel, label, painter, widget)
            
        if option.subControls & QStyle.SC_ToolButtonMenu:
            tool.state = mflags
            tool.rect = menuRect.adjusted(1, 1, -1, -1)
            if mflags & (QStyle.State_Sunken | QStyle.State_On | QStyle.State_Raised):
                painter.setPen(Qt.gray)
                painter.drawLine(tool.rect.topLeft(), tool.rect.bottomLeft())
                if mflags & QStyel.State_Sunken:
                    shade = QColor(0, 0, 0, 50)
                    painter.fillRect(tool.rect.adjusted(0, -1, 1, 1), shade)
                elif mflags & QStyel.State_MouseOver:
                    shade = QColor(255, 255, 255, 50)
                    painter.fillRect(tool.rect.adjusted(0, -1, 1, 1), shade)
            tool.rect = tool.rect.adjusted(2, 2, -2, -2)
            self.draw_IndicatorArrowDown(tool, painter, widget)
        elif option.features & QStyleOptionToolButton.HasMenu:
            arrowSize = 6
            ir = option.rect.adjusted(1, 1, -1, -1)
            newBtn = QStyleOptionToolButton(option)
            newBtn.palette = self.panelPalette(option.palette)
            newBtn.rect = QRect(ir.right() - arrowSize - 1,
                                ir.height() - arrowSize - 2, arrowSize, arrowSize)
            self.draw_IndicatorArrowDown(newBtn, painter, widget)
    
    def draw_PanelLineEdit(self, option, painter, widget):
        painter.save()
        filledRect = option.rect.adjusted(1, 1, -1, -1)
        painter.setBrushOrigin(filledRect.topLeft())
        painter.fillRect(filledRect, option.palette.base())
        
        if option.state & State_Enabled:
            self.drawCornerImage(self.lineeditImage, painter, option.rect, 2, 2, 2, 2)
        else:
            self.drawCornerImage(self.lineeditImage_disabled, painter, option.rect, 2, 2, 2, 2)

        if option.state & State_HasFocus or option.state & State_MouseOver:
            hover = QColor(theme.baseColor)
            if state & State_HasFocus:
                hover.setAlpha(100)
            else:
                hover.setAlpha(50)
            painter.setPen(QPen(hover, 1))
            painter.drawRect(option.rect.adjusted(1, 1, -2 ,-2))
        painter.restore()
    
fancystyle = FancyStyle()
